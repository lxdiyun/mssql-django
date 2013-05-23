# -*- coding: utf-8 -*-
AREA_DICT = {
    1: (u"一楼西区", u"外文图书"),
    2: (u"一楼西北区", u"N"),
    3: (u"一楼西南区", u"A,N"),
    4: (u"一楼东南区", u"A"),
    5: (u"一夹层西北区", u"X"),
    6: (u"一夹层东南区", u"A"),
    7: (u"二夹层西北区", u"Q"),
    8: (u"二夹层东北区", u"C,Q,R,S,U,V"),
    9: (u"二夹层东南区", u"C"),
    10: (u"二夹层西南区", u"C,P"),
    11: (u"二楼西区", u"K"),
    12: (u"二楼西北区外侧", u"T-TP"),
    13: (u"二楼西北区内侧", u"TP,TU"),
    14: (u"二楼北区", u"O"),
    15: (u"二楼东北区", u"E,Z,TS,TQ"),
    16: (u"二楼东南区", u"B"),
    17: (u"二楼南区", u"B"),
    18: (u"二楼西南区", u"K"),
    19: (u"三楼西区", u"F"),
    20: (u"三楼西北区外侧", u"F"),
    21: (u"三楼西北区内侧", u"G,J"),
    22: (u"三楼北区", u"D"),
    23: (u"三楼东北区", u"I"),
    24: (u"三楼西南区", u"H"),
    25: (u"三楼特区", u"特藏"),
    26: (u"二楼专题区", u""),
    27: (u"三楼专题区", u""),
    28: (u"一楼东区", u"期刊合订本"),
}

CATALOG_DICT = {
    1: ("A", u"A"),
    2: ("B", u"B"),
    3: ("C", u"C"),
    4: ("D", u"D"),
    5: ("E", u"E"),
    6: ("F", u"F"),
    7: ("G", u"G"),
    8: ("H", u"H"),
    9: ("I", u"I"),
    10: ("J", u"J"),
    11: ("K", u"K"),
    12: ("N", u"N"),
    13: ("O", u"O"),
    14: ("P", u"P"),
    15: ("Q", u"Q"),
    16: ("R", u"R"),
    17: ("S", u"S"),
    18: ("T", u"T"),
    19: ("U", u"U"),
    20: ("V", u"V"),
    21: ("X", u"X"),
    22: ("Z", u"Z"),
    23: ("TB", u"TB"),
    24: ("TD", u"TD"),
    25: ("TE", u"TE"),
    26: ("TG", u"TG"),
    27: ("TH", u"TH"),
    28: ("TK", u"TK"),
    29: ("TL", u"TL"),
    30: ("TM", u"TM"),
    31: ("TN", u"TN"),
    32: ("TP", u"TP"),
    33: ("TQ", u"TQ"),
    34: ("TS", u"TS"),
    35: ("TU", u"TU"),
    36: ("TV", u"TV"),
}


def trans_case_no_without_area(case_no):
        info = ""

        if "" != case_no:
            row_no = int(case_no[6:9])
            line_no = int(case_no[9:-2])
            layer_no = int(case_no[-2:])

            if 999 == row_no:
                info += u"壁面架%d列%d层" % (line_no, layer_no)
            elif 888 == row_no:
                info += u"矮层架%d列%d层" % (line_no, layer_no)
            else:
                info += u"%d排%d列%d层" % (row_no, line_no, layer_no)

        return info


def trans_case_no(case_no):
        global AREA_DICT
        info = ""

        if "" != case_no:
            area = int(case_no[:6])

            if area in AREA_DICT:
                info += AREA_DICT[area][0]

        return info + trans_case_no_without_area(case_no)
