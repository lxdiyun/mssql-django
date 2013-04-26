# -*- coding: utf-8 -*-
from checkcase.models import Bookcaseidinfo
from rfid.models import Bookinfo


def check_special(p, n):
    special = {
        # O 类 柱子
        '00001400700306': '00001400700901',
        '00001400800906': '00001400800301',
        # 外文 并排
        '00000101800106': '00000101500801',
        '00000101400806': '00000101900101',
        '00000102000106': '00000101300801',
        # 二夹层东北区 C,Q 类交界
        '00000899900105': '00000899903201',
        '00001799901202': '00001799901102',

        # 二楼南区 B 类 高层套书
        '00001799901102': '00001799901002',
        '00001799901002': '00001799900902',
        '00001799900902': '00001799900702',
        '00001799900702': '00001799900802',
        '00001799900802': '00001799900101',

        # 三楼西北区内侧 G,J交界
        '00002103700306': '00002100100301',

        # 二楼东北区 E,Z交界
        '00001599902006': '00001599900101',
    }

    key = p.szbookcaseno
    if key in special:
        if n.szbookcaseno == special[key]:
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

#    prin(p_row_no, m_row_no, m_layer_no)
    return check_special(p, n)


def check_cases(cases):
    pre_case = None
    current_case = None
    next_case = None
    case_id_list = list(int(case.szbookcaseno) for case in cases)
    error_list = list()
    book_id_list = list(case.szfirstbookid for case in cases)
    books = list(Bookinfo.objects.filter(szbookid__in=book_id_list))
    book_dict = dict((book.szbookid, book) for book in books)

    for case in cases:
        next_case = case
        case.is_error = False
        if case.szfirstbookid in book_dict:
            case.book = book_dict[case.szfirstbookid]
            if case.book.bforcesortcase:
                case.is_warning = True
            if current_case:
                if not check_case(current_case, next_case, case_id_list):
                    case.is_error = True
        else:
            case.is_error = True

        if case.is_error:
            error_case = {"pre": pre_case,
                          "cur": current_case,
                          "next": next_case}
            error_list.append(error_case)
        else:
            case_id_list.remove(int(case.szbookcaseno))
        pre_case = current_case
        current_case = next_case

    return {
        "error_list": error_list,
        "count": cases.count(),
        "all_cases": cases
    }


def check_area(area_prefix):
    area = "%06d" % area_prefix
    cases = Bookcaseidinfo.objects.exclude(szfirstbookid__isnull=True)
    cases = cases.exclude(szfirstbookid__exact='')
    cases = cases.filter(szbookcaseno__startswith=area)
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
