# -*- coding: utf-8 -*-
from checkcase.models import Bookcaseidinfo, Bookinfo


def check_special(p, m, n):
    special = {
        # O 类 柱子
        '00001400700902': '00001400700306',
        '00001400800302': '00001400800906',
        '00001400700901': '00001400700305',
        '00001400800301': '00001400800905',
        # 外文 壁面
        '00000101600101': '00000199901205',
        '00000101600102': '00000199901206',
        '00000199901101': '00000100100105',
        '00000199901102': '00000100100106',
        '00000102100101': '00000199900105',
        '00000102100102': '00000199900106',
        # 二夹层东北区 C,Q 类交界
        "00000899903201": "00000899900104",
        "00000899903202": "00000899900105",
    }

    key = n.szbookcaseno
    if key in special:
        if p.szbookcaseno == special[key]:
            return True

    return False


def check_case(p, m, n):
    p_no = int(p.szbookcaseno)
    m_no = int(m.szbookcaseno)
    n_no = int(n.szbookcaseno)
    p_row_no = int(p.szbookcaseno[7:9])
    n_row_no = int(n.szbookcaseno[7:9])
    n_layer_no = int(n.szbookcaseno[-2:])

    # 层变换
    if 2 == (n_no - p_no):
        return True

    # 列变换（逆序,6层）
    if 104 == (p_no - n_no):
        return True
    # 列变换（逆序,5层）
    if 103 == (p_no - n_no):
        return True
    # 列变换（逆序,3层）
    if 101 == (p_no - n_no):
        return True
    # 列变换（正序,6层）
    if 96 == (n_no - p_no):
        return True
    # 列变换（正序,5层）
    if 97 == (n_no - p_no):
        return True
    # 列变换（正序,3层）
    if 99 == (n_no - p_no):
        return True

    # 排变换
    if n_row_no != p_row_no:
        if ((1 == m_no - p_no) and (1 == n_layer_no)):
            return True
        if ((1 == n_no - m_no) and (2 == n_layer_no)):
            return True

#    prin(p_row_no, m_row_no, m_layer_no)
    return check_special(p, m, n)


def main():
    global g_reverse
    cases = Bookcaseidinfo.objects.exclude(szfirstbookid__isnull=True)
    cases = cases.exclude(szfirstbookid__exact='')
    cases = cases.filter(szbookcaseno__startswith="000015")
    cases = cases.order_by('szpretendindexnum')
    pre_case = None
    current_case = None
    next_case = None
    g_reverse = False
    for case in cases:
#        print(case.szbookcaseno)
        next_case = case
        if pre_case and current_case:
            if not check_case(pre_case, current_case, next_case):
                print("%s <= %s => %s \n" % (pre_case.szbookcaseno,
                                             current_case.szbookcaseno,
                                             next_case.szbookcaseno))
#                print("\"%s\": \"%s\"," % (next_case.szbookcaseno,
#                                           pre_case.szbookcaseno))
        pre_case = current_case
        current_case = next_case
    print(cases.count())
