# -*- coding: utf-8 -*-
from checkcase.models import Bookcaseidinfo, Bookinfo


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

    if (n_no - 1) not in case_list:
        if (p_no + 1) not in case_list:
            if 1 == abs(n_line_no - p_line_no):
                return True

    return False


def check_line_change_999(p, n, case_list):
    p_no = int(p.szbookcaseno)
    n_no = int(n.szbookcaseno)
    p_row_no = int(p.szbookcaseno[6:9])
    n_row_no = int(n.szbookcaseno[6:9])

    if (n_no - 1) not in case_list:
        if (p_no + 1) not in case_list:
            if 999 == n_row_no and 999 != p_row_no:
                return True
            elif 999 == p_row_no and 999 != n_row_no:
                return True

    return False


def check_case(p, n, case_list):
    p_no = int(p.szbookcaseno)
    n_no = int(n.szbookcaseno)
    p_row_no = int(p.szbookcaseno[6:9])
    n_row_no = int(n.szbookcaseno[6:9])
    n_no = int(n.szbookcaseno)

    # 层变换
    if 1 == (n_no - p_no):
        return True

    # 列变化
    if check_line_change(p, n, case_list):
        return True

    # 排变换
    if n_row_no != p_row_no:
        if ((1 == abs(p_row_no - n_row_no)) and (n_no - 1) not in case_list):
            return True

    # 壁面价变化
    if check_line_change_999(p, n, case_list):
        return True

#    prin(p_row_no, m_row_no, m_layer_no)
    return check_special(p, n)


def check_cases(cases):
    pre_case = None
    current_case = None
    next_case = None
    case_list = list(int(case.szbookcaseno) for case in cases)
    for case in cases:
#        print(case.szbookcaseno)
        next_case = case
        if current_case:
            if not check_case(current_case, next_case, case_list):
                if pre_case:
                    pre_case_no = pre_case.szbookcaseno
                else:
                    pre_case_no = None
                print("%s <= %s => %s" % (pre_case_no,
                                          current_case.szbookcaseno,
                                          next_case.szbookcaseno))
#                print("'%s': '%s',\n" % (current_case.szbookcaseno,
#                                         next_case.szbookcaseno))
            else:
                case_list.remove(int(current_case.szbookcaseno))
        pre_case = current_case
        current_case = next_case
    print(cases.count())


def main(prefix):
    area = "%06d" % prefix
    cases = Bookcaseidinfo.objects.exclude(szfirstbookid__isnull=True)
    cases = cases.exclude(szfirstbookid__exact='')
    cases = cases.filter(szbookcaseno__startswith=area)
    cases = cases.order_by('szpretendindexnum')
    check_cases(cases)
