# -*- coding: utf-8 -*-
from checkcase.models import Bookcaseidinfo, Bookinfo


def check_case(pre, current):
    pre_no = int(pre.szbookcaseno)
    current_no = int(current.szbookcaseno)
    pre_row_no = int(pre.szbookcaseno[7:9])
    current_row_no = int(current.szbookcaseno[7:9])
    current_layer_no = int(current.szbookcaseno[-2:])

    # 层变换
    if 1 == (current_no - pre_no):
        return True
    # 列变换（正序,6层）
    elif 95 == (current_no - pre_no):
        return True
    # 列变换（逆序,6层）
    elif 105 == (pre_no - current_no):
        return True
    # 列变换（正序,5层）
    elif 96 == (current_no - pre_no):
        return True
    # 列变换（逆序,5层）
    elif 104 == (pre_no - current_no):
        return True
    # 列变换（正序,3层）
    elif 98 == (current_no - pre_no):
        return True
    # 列变换（逆序,3层）
    elif 102 == (pre_no - current_no):
        return True
    # 排变换
    elif ((1 == (current_row_no - pre_row_no))
          and (1 == current_layer_no)):
        return True

#    print(pre_row_no, current_row_no, current_layer_no)
    return False


def main():

    cases = Bookcaseidinfo.objects.exclude(szfirstbookid__isnull=True)
    cases = cases.exclude(szfirstbookid__exact='')
    cases = cases.filter(szbookcaseno__startswith="000024")
    cases = cases.order_by('szpretendindexnum')
    last_case = None
    for case in cases:
        if last_case:
            if not check_case(last_case, case):
                print("%s => %s" % (last_case.szbookcaseno,
                                    case.szbookcaseno))
        last_case = case
    print(cases.count())
