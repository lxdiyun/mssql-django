# -*- coding: utf-8 -*-
from django.db import models
from rfid.utils import trans_case_no_without_area


class Bookcaseidinfo(models.Model):
    nbookcaseid = models.TextField(db_column='nBookCaseID', blank=True)
    nepcorder = models.IntegerField(null=True,
                                    db_column='nEPCOrder',
                                    blank=True)
    nlayer = models.IntegerField(db_column='nLayer')
    dtlastordercase = models.DateTimeField(null=True,
                                           db_column='dtLastOrderCase',
                                           blank=True)
    dtlastmatchcase = models.DateTimeField(null=True,
                                           db_column='dtLastMatchCase',
                                           blank=True)
    dtlastupdate = models.DateTimeField(null=True,
                                        db_column='dtLastUpdate',
                                        blank=True)
    nonnum = models.IntegerField(null=True, db_column='nOnNum', blank=True)
    nwrongnum = models.IntegerField(null=True,
                                    db_column='nWrongNum',
                                    blank=True)
    szbookcaseno = models.TextField(primary_key=True, db_column='szBookCaseNo')
    norder = models.IntegerField(null=True, db_column='nOrder', blank=True)
    nbookcount = models.IntegerField(null=True,
                                     db_column='nBookCount',
                                     blank=True)
    nbookcaseinfoid = models.IntegerField(null=True,
                                          db_column='nBookCaseInfoID',
                                          blank=True)
    szfirstbookid = models.TextField(db_column='szFirstBookID', blank=True)
    nid = models.IntegerField(db_column='nID')
    szpretendindexnum = models.TextField(db_column='szPretendIndexNum',
                                         blank=True)
    szcasenotrans = models.TextField(db_column='szCaseNoTrans', blank=True)
    szlibcd = models.TextField(db_column='szlibCD', blank=True)

    class Meta:
        db_table = 'BookCaseIDInfo'

    def __unicode__(self):
        return self.szbookcaseno

    def translate(self):
        return trans_case_no_without_area(self.szbookcaseno)
