# -*- coding: utf-8 -*-
from checkcase.models import Bookcaseidinfo
from rfid.models import Bookinfo


def check_special(p, n):
    special = {
        # 二楼北区 O 类 柱子
        '00001400700306': '00001400700901',
        '00001400800906': '00001400800301',
        # 一楼西区 外文 并排
        '00000101600806': '00000101700101',
        '00000101800106': '00000101500801',
        '00000101400806': '00000101900101',
        '00000102000106': '00000101300801',
        # 二夹层东北区 C,Q 类交界
        '00000899900105': '00000899903201',
        '00001799901202': '00001799901102',

        # 二楼南区 B 类 高层套书
        '00001799901102': '00001799901002',
        '00001799901002': '00001799900902',
        '00001799900902': '00001799900802',
        '00001799900802': '00001799900702',

        # B类 二楼东南区 南区交界
        '00001799900702': '00001600201201',
        '00001699901205': '00001799900101',
        '00001700100106': '00001600202401',
        '00001600102403': '00001700200101',
        '00001799900707': '00001699901101',

        # 三楼西北区内侧 G,J交界
        '00002103700306': '00002100100301',

        # 二楼东北区 E,Z交界
        '00001599902006': '00001599900101',

        # 三楼东北区 I 类 柱子 长短架交界
        '00002300400306': '00002300500701',
        '00002300600706': '00002300700601',
        '00002300800606': '00002300900801',
        '00002301600806': '00002301700601',
        '00002301800606': '00002301900801',
        '00002302600806': '00002302700701',
        '00002302800706': '00002302900801',
        '00002303400806': '00002303500301',
    }

    key = p.szbookcaseno
    if key in special:
        if n.szbookcaseno == special[key]:
            p.is_success = True
            n.is_success = True
            return True

    return False


def check_line_change(p, n, case_list):
    p_no = int(p.szbookcaseno)
    n_no = int(n.szbookcaseno)
    p_line_no = int(p.szbookcaseno[-4:-2])
    n_line_no = int(n.szbookcaseno[-4:-2])
    p_row_no = int(p.szbookcaseno[6:9])
    n_row_no = int(n.szbookcaseno[6:9])

    if (n_no - 1) not in case_list:
        if (p_no + 1) not in case_list:
            if 1 == abs(n_line_no - p_line_no):
                if p_row_no == n_row_no:
                    return True

    return False


def check_row_change(p, n, case_list):
    p_no = int(p.szbookcaseno)
    n_no = int(n.szbookcaseno)
    p_row_no = int(p.szbookcaseno[6:9])
    n_row_no = int(n.szbookcaseno[6:9])
    p_line_no = int(p.szbookcaseno[-4:-2])
    n_line_no = int(n.szbookcaseno[-4:-2])

    if ((p_no + 1) not in case_list) and ((n_no - 1) not in case_list):
        if p_line_no == n_line_no:
            if 1 == abs(p_row_no - n_row_no):
                return True

    return False


def check_row_change_999(p, n, case_list):
    p_no = int(p.szbookcaseno)
    n_no = int(n.szbookcaseno)
    p_row_no = int(p.szbookcaseno[6:9])
    n_row_no = int(n.szbookcaseno[6:9])

    if ((n_no - 1) not in case_list) and ((p_no + 1) not in case_list):
        if 999 == n_row_no and 999 != p_row_no:
            return True
        elif 999 == p_row_no and 999 != n_row_no:
            return True

    return False


def check_case(p, n, case_list):
    p_no = int(p.szbookcaseno)
    n_no = int(n.szbookcaseno)
    p_area_no = int(p.szbookcaseno[:6])
    n_area_no = int(n.szbookcaseno[:6])

    # 层变换
    if 1 == (n_no - p_no):
        return True

    # 列变化
    if check_line_change(p, n, case_list):
        return True

    # 排变换
    if check_row_change(p, n, case_list):
        return True

    # 壁面架变化
    if check_row_change_999(p, n, case_list):
        return True

    # 区域变换
    if p_area_no != n_area_no:
        p.is_info = True
        n.is_info = True

    # 首书重复
    if p.szfirstbookid == n.szfirstbookid:
        return False

#    prin(p_row_no, m_row_no, m_layer_no)
    return check_special(p, n)


# we need this function cause sqlserver 2005 has 2100 parameters limits
def get_books(book_id_list):
    index = 0
    books = list()
    while index < len(book_id_list):
        books += Bookinfo.objects.filter(
            szbookid__in=book_id_list[index:index+2000])
        index += 2000

    return books


def check_cases(cases):
    pre_case = None
    current_case = None
    next_case = None
    error_count = 0
    warning_count = 0
    case_id_list = list(int(case.szbookcaseno) for case in cases)
    error_list = list()
    book_id_list = list(case.szfirstbookid for case in cases)
    books = get_books(book_id_list)
    book_dict = dict((book.szbookid, book) for book in books)

    for case in cases:
        next_case = case
        case.is_error = False
        case.is_warning = False
        if case.szfirstbookid in book_dict:
            case.book = book_dict[case.szfirstbookid]
            if case.book.bforcesortcase:
                case.is_warning = True

            if case.book.szpretendindexnum != case.szpretendindexnum:
                case.is_warning = True

            if current_case:
                if not check_case(current_case, next_case, case_id_list):
                    case.is_error = True
        else:
            case.is_error = True

        if case.is_error:
            error_count += 1
            error_case = {"pre": pre_case,
                          "cur": current_case,
                          "next": next_case}
            error_list.append(error_case)
        else:
            case_id_list.remove(int(case.szbookcaseno))

        if case.is_warning:
                warning_count += 1

        pre_case = current_case
        current_case = next_case

    print error_count, warning_count

    return {
        "error_list": error_list,
        "total_count": cases.count(),
        "error_count": error_count,
        "warning_count": warning_count,
        "all_cases": cases
    }


def check_area(area_prefix):
    area = "%06d" % area_prefix
    cases = Bookcaseidinfo.objects.exclude(szfirstbookid__isnull=True)
    cases = cases.exclude(szfirstbookid__exact='')
    cases = cases.filter(szbookcaseno__startswith=area)
    cases = cases.order_by('szpretendindexnum')

    return check_cases(cases)


def check_catalog(catalog_prefix):
    cases = Bookcaseidinfo.objects.all()
    cases = Bookcaseidinfo.objects.exclude(szfirstbookid__isnull=True)
    cases = cases.exclude(szfirstbookid__exact='')
    cases = cases.filter(szpretendindexnum__startswith=catalog_prefix)
    cases = cases.order_by('szpretendindexnum')

    return check_cases(cases)


def main(area):
    error_dict = check_area(area)
    print(error_dict['count'])

    for error_case in error_dict['error_list']:
        pre_case = error_case["pre"]
        current_case = error_case["cur"]
        next_case = error_case["next"]
        if pre_case:
            pre_case_no = pre_case.szbookcaseno
            print("%s <= %s => %s" % (pre_case_no,
                                      current_case.szbookcaseno,
                                      next_case.szbookcaseno))
#            print("'%s': '%s',\n" % (current_case.szbookcaseno,
#                                     next_case.szbookcaseno))
        else:
            pre_case_no = None
