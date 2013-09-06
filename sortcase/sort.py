from rfid.models import Bookinfo, Bookcaseidinfo
from re import sub


def sort_books(case_no, start_index, end_index):
    #    print(case_no, start_index, end_index)
    # clean up old books
    books = Bookinfo.objects.all()
    books = books.filter(bforcesortcase=0)
    books = books.filter(szbookcaseno=case_no)
    #    print('before: %d' % len(books))
    books.update(szbookcaseno='')

    # update new books
    books = Bookinfo.objects.all()
    books = books.filter(szpretendindexnum__gte=start_index)
    books = books.filter(szpretendindexnum__lt=end_index)
    books = books.filter(bforcesortcase=0)
    #    print('after: %d' % len(books))
    books.update(szbookcaseno=case_no)


def sort_cases(cases, across_catalog=False):
    count = 1
    total = len(cases)
    pre_case = None
    for case in cases:
        print("[%d/%d] %s %s %s" % (count,
                                    total,
                                    case.szbookcaseno,
                                    case.szfirstbookid,
                                    case.szpretendindexnum))
        if 1 < count:
            start_index = pre_case.szpretendindexnum
            end_index = case.szpretendindexnum
            start_prefix = sub(r'^(\d*[a-zA-Z]).*$', r'\g<1>', start_index)
            end_prefix = sub(r'^(\d*[a-zA-Z]).*$', r'\g<1>', end_index)

            if (start_prefix != end_prefix) and (across_catalog is not True):
                print('Warning catalog change at %s ------------------'
                      % case.szbookcaseno)
                end_index = start_prefix + "{{{"

            sort_books(pre_case.szbookcaseno, start_index, end_index)

        if count == total:
            start_index = case.szpretendindexnum
            end_index = sub(r'^(\d*[a-zA-Z]+).*$',
                            r'\g<1>{{{',
                            case.szpretendindexnum)
            if "0113TD{{{" == end_index:
                end_index = "0114TE{{{"
            sort_books(case.szbookcaseno, start_index, end_index)

        count += 1
        pre_case = case


def sort_area(area_prefix):
    cases = Bookcaseidinfo.get_cases_by_area(area_prefix)

    if 1 == area_prefix:
        sort_cases(cases, across_catalog=True)
    else:
        sort_cases(cases)


def sort_catalog(catalog_prefix):
    cases = Bookcaseidinfo.get_cases_by_catalog(catalog_prefix)

    sort_cases(cases)
