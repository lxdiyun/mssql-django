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
    1: ("A", u"0101A", 0),
    2: ("B", u"0131B", 539),
    3: ("C", u"0104C", 0),
    4: ("D", u"0135D", 1248),
    5: ("E", u"0126E", 0),
    6: ("F", u"0132F", 2214),
    7: ("G", u"0133G", 0),
    8: ("H", u"0137H", 1190),
    9: ("I", u"0136I", 1704),
    10: ("J", u"0134J", 0),
    11: ("K", u"0110K", 1040),
    12: ("N", u"0100N", 0),
    13: ("O", u"0125O", 468),
    14: ("P", u"0109P", 0),
    15: ("Q", u"0103Q", 0),
    16: ("R", u"0105R", 0),
    17: ("S", u"0106S", 0),
    18: ("T", u"0111T", 0),
    19: ("U", u"0107U", 0),
    20: ("V", u"0108V", 0),
    21: ("X", u"0102X", 75),
    22: ("Z", u"0127Z", 0),
    23: ("TB", u"0112TB", 0),
    24: ("TD", u"0113TD", 0),
    25: ("TE", u"0114TE", 0),
    26: ("TF", u"0115TF", 0),
    27: ("TG", u"0116TG", 0),
    28: ("TH", u"0117TH", 0),
    29: ("TJ", u"0118TJ", 0),
    30: ("TK", u"0119TK", 0),
    31: ("TL", u"0120TL", 0),
    32: ("TM", u"0121TM", 0),
    33: ("TN", u"0122TN", 0),
    34: ("TP", u"0123TP", 0),
    35: ("TQ", u"0129TQ", 0),
    36: ("TS", u"0128TS", 0),
    37: ("TU", u"0124TU", 0),
    38: ("TV", u"0130TV", 0),
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
