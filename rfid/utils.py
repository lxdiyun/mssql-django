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
    1: ("A", u"01A"),
    2: ("B", u"0132B"),
    3: ("C", u"01C"),
    4: ("D", u"01D"),
    5: ("E", u"01E"),
    6: ("F", u"01F"),
    7: ("G", u"01G"),
    8: ("H", u"01H"),
    9: ("I", u"01I"),
    10: ("J", u"01J"),
    11: ("K", u"01K"),
    12: ("N", u"01N"),
    13: ("O", u"0125O"),
    14: ("P", u"01P"),
    15: ("Q", u"01Q"),
    16: ("R", u"01R"),
    17: ("S", u"01S"),
    18: ("T", u"01T"),
    19: ("U", u"01U"),
    20: ("V", u"01V"),
    21: ("X", u"01X"),
    22: ("Z", u"01Z"),
    23: ("TB", u"01TB"),
    24: ("TD", u"01TD"),
    25: ("TE", u"01TE"),
    26: ("TG", u"01TG"),
    27: ("TH", u"01TH"),
    28: ("TK", u"01TK"),
    29: ("TL", u"01TL"),
    30: ("TM", u"01TM"),
    31: ("TN", u"01TN"),
    32: ("TP", u"01TP"),
    33: ("TQ", u"01TQ"),
    34: ("TS", u"01TS"),
    35: ("TU", u"01TU"),
    36: ("TV", u"01TV"),
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
