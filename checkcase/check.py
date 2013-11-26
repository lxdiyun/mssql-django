# -*- coding: utf-8 -*-
from rfid.models import Bookinfo, Bookcaseidinfo

CHECKED_CATALOG_LIST = ['C', 'B', 'E', 'F', 'I', 'K', 'N', 'O', 'P', 'Q', 'R',
                        'S', 'T', 'U', 'V', 'Z',
                        'TB', 'TD', 'TE', 'TF', 'TG', 'TH', 'TJ', 'TK', 'TL',
                        'TM', 'TN', 'TP', 'TQ', 'TS', 'TU', 'TV', ]


def check_special(p, n):
    special = {
        # 一楼西区 外文 并排
        '00000101600806': '00000101700101',
        '00000101800106': '00000101500801',
        '00000101400806': '00000101900101',
        '00000102000106': '00000101300801',

        # 一楼西南区 A,N 类
        '00000399901204': '00000399900102',

        # 二夹层 C,Q,R,S,U,V 类交界
        '00000899900105': '00000899902501',
        '00001099903606': '00001099900102',

        # 二楼北区 O 类 柱子
        '00001400700306': '00001400700901',
        '00001400800906': '00001400800301',

        # 二楼东南区 B 类 楼梯间断
        '00001600101403': '00001600201401',
        '00001600201503': '00001600101501',

        # 二楼东北区 E,Z,TS,TQ 类交界
        '00001599902006': '00001599900101',
        '00001599900806': '00001599901605',
        '00001599902006': '00001599900901',

        # 二楼西区 K类 柱子
        '00001100500406': '00001100500201',
        '00001100600206': '00001100600401',

        # 三楼西北区内侧 G,J交界
        '00002103700306': '00002100100301',
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
        if 1 == abs(p_row_no - n_row_no):
            if (p_line_no == n_line_no) and (1 == p_line_no):
                return True
            elif ((p_no + 100) not in case_list) and ((n_no + 100) not in
                                                      case_list):
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

    # 首书重复
    if p.firstbook == n.firstbook:
        return False

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
        result = True
        # 连续跨区是错误
        if p.across_area:
            result = False

        p.across_area = True
        n.across_area = True
        p.is_info = True
        n.is_info = True

        return result

#    prin(p_row_no, m_row_no, m_layer_no)
    return check_special(p, n)


def check_cases(cases):
    pre_case = None
    current_case = None
    next_case = None
    error_count = 0
    warning_count = 0
    case_id_list = list(int(case.szbookcaseno) for case in cases)
    error_list = list()

    for case in cases:
        next_case = case
        case.is_error = False
        case.is_warning = False
        case.across_area = False
        if case.firstbook:
            if case.szbookcaseno != case.firstbook.szbookcaseno:
                case.is_warning = True

            if case.firstbook.szpretendindexnum != case.szpretendindexnum:
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

    return {
        "error_list": error_list,
        "total_count": len(cases),
        "error_count": error_count,
        "warning_count": warning_count,
        "all_cases": cases
    }


def check_area(area_prefix):
    cases = Bookcaseidinfo.get_cases_by_area(area_prefix)

    # 外文伪索书号分类不需要区分前缀
    if 1 == area_prefix:
        cases = sorted(cases, key=lambda case: case.szpretendindexnum[4:])

    return check_cases(cases)


def check_catalog(catalog_prefix):
    cases = Bookcaseidinfo.get_cases_by_catalog(catalog_prefix)

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
