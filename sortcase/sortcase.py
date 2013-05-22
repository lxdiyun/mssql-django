from checkcase.models import Bookcaseidinfo
from rfid.models import Bookinfo
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


def sort_cases(cases):
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
            start_prefix = sub(r'^(\d*[a-zA-Z]+).*$', r'\g<1>', start_index)
            end_prefix = sub(r'^(\d*[a-zA-Z]+).*$', r'\g<1>', end_index)

            if start_prefix != end_prefix:
                print('Warning catalog change at %s ------------------'
                      % case.szbookcaseno)

            sort_books(pre_case.szbookcaseno, start_index, end_index)

        if count == total:
            start_index = case.szpretendindexnum
            end_index = sub(r'^(\d*[a-zA-Z]+).*$',
                            r'\g<1>\\x453{{{',
                            case.szpretendindexnum)
            sort_books(case.szbookcaseno, start_index, end_index)

        count += 1
        pre_case = case


def sort_area(area_prefix):
    area = "%06d" % area_prefix
    cases = Bookcaseidinfo.objects.exclude(szfirstbookid__isnull=True)
    cases = cases.exclude(szfirstbookid__exact='')
    cases = cases.filter(szbookcaseno__startswith=area)
    cases = cases.order_by('szpretendindexnum')

    sort_cases(cases)


def sort_catalog(catalog_prefix):
    cases = Bookcaseidinfo.objects.all()
    cases = Bookcaseidinfo.objects.exclude(szfirstbookid__isnull=True)
    cases = cases.exclude(szfirstbookid__exact='')
    cases = cases.filter(szpretendindexnum__startswith=catalog_prefix)
    cases = cases.order_by('szpretendindexnum')

    sort_cases(cases)
