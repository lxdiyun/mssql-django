# -*- coding: utf-8 -*-

from django.db import models
from utils import trans_case_no
from urllib import quote
from re import sub


class Bookinfo(models.Model):
    nlabelid = models.TextField(db_column='nLabelID', blank=True)
    nepcorder = models.IntegerField(null=True,
                                    db_column='nEPCOrder',
                                    blank=True)
    szbookcaseno = models.TextField(db_column='szBookCaseNo', blank=True)
    nbookstypeid = models.IntegerField(null=True, db_column='nBooksTypeID',
                                       blank=True)
    npublishid = models.IntegerField(null=True,
                                     db_column='nPublishID',
                                     blank=True)
    szbookssid = models.TextField(db_column='szBookSSID')
    szseriesid = models.TextField(db_column='szSeriesID', blank=True)
    nbookstatus = models.IntegerField(null=True,
                                      db_column='nBookStatus',
                                      blank=True)
    szcardid = models.TextField(db_column='szCardID', blank=True)
    dtborrowdate = models.DateTimeField(null=True,
                                        db_column='dtBorrowDate',
                                        blank=True)
    dtneedbackdate = models.DateTimeField(null=True,
                                          db_column='dtNeedBackDate',
                                          blank=True)
    dtlastread = models.DateTimeField(null=True,
                                      db_column='dtLastRead',
                                      blank=True)
    nstaffid = models.IntegerField(null=True, db_column='nStaffID', blank=True)
    szbookid = models.TextField(primary_key=True, db_column='szBookID')
    szisbn = models.TextField(db_column='szISBN', blank=True)
    szname = models.TextField(db_column='szName', blank=True)
    szauthor = models.TextField(db_column='szAuthor', blank=True)
    fprice = models.DecimalField(decimal_places=2,
                                 null=True,
                                 max_digits=10,
                                 db_column='fPrice',
                                 blank=True)
    dtpublishdate = models.DateTimeField(null=True,
                                         db_column='dtPublishDate',
                                         blank=True)
    npages = models.IntegerField(null=True, db_column='nPages', blank=True)
    szbookindex = models.TextField(db_column='szBookIndex', blank=True)
    szmainword = models.CharField(max_length=50,
                                  db_column='szMainWord',
                                  blank=True)
    szclassno = models.TextField(db_column='szClassNO', blank=True)
    szlibcd = models.TextField(db_column='szlibCD', blank=True)
    szmemo = models.TextField(db_column='szMemo', blank=True)
    nstartyear = models.IntegerField(null=True,
                                     db_column='nStartYear',
                                     blank=True)
    szpublishyear = models.TextField(db_column='szPublishyear', blank=True)
    nconvertstaffid = models.IntegerField(null=True,
                                          db_column='nConvertStaffID',
                                          blank=True)
    dtconvertdate = models.DateTimeField(null=True,
                                         db_column='dtConvertDate',
                                         blank=True)
    nupdatestaffid = models.IntegerField(null=True,
                                         db_column='nUpdateStaffID',
                                         blank=True)
    dtupdatedate = models.DateTimeField(null=True,
                                        db_column='dtUpdateDate',
                                        blank=True)
    szmoneytype = models.TextField(db_column='szMoneyType', blank=True)
    szpretendindexnum = models.TextField(db_column='szPretendIndexNum',
                                         blank=True)
    bforcesortcase = models.NullBooleanField(null=True,
                                             db_column='bForceSortCase',
                                             blank=True)
    szconvertstaff = models.TextField(db_column='szConvertStaff', blank=True)
    dtautoupdate = models.DateTimeField(null=True,
                                        db_column='dtAutoUpdate',
                                        blank=True)
    nrenewtime = models.IntegerField(null=True,
                                     db_column='nRenewTime',
                                     blank=True)
    nbooklentype = models.IntegerField(null=True,
                                       db_column='nBookLenType',
                                       blank=True)
    szbooklen = models.TextField(db_column='szBookLen', blank=True)
    nbookthickness = models.IntegerField(null=True,
                                         db_column='nBookThickness',
                                         blank=True)
    nsetinfocount = models.IntegerField(null=True,
                                        db_column='nSetInfoCount',
                                        blank=True)
    nsetinfoorder = models.IntegerField(null=True,
                                        db_column='nSetInfoOrder',
                                        blank=True)
    sztemplibcd = models.TextField(db_column='szTemplibCD', blank=True)
    szmedicallib = models.TextField(db_column='szMedicalLib', blank=True)

    class Meta:
        db_table = 'BookInfo'

    def get_case_info(self):
        return trans_case_no(self.szbookcaseno)

    def get_search_url(self):
        url = ("http://202.192.155.48:83/opac/searchresult.aspx?"
               "callno_f=%s"
               "&dt=ALL&cl=ALL&dp=20&sf=M_PUB_YEAR"
               "&ob=DESC&sm=table&dept=ALL&st=2&ecx=0&efz=0")
        callno = sub("([^/]*)/([^/]*)(/.*)?$",
                     "\g<1>/\g<2>",
                     self.szbookindex)

        return url % quote(callno.encode("gb18030", 'replace'))

    # we need this function cause sqlserver 2005 has 2100 parameters limits
    @staticmethod
    def get_books(book_id_list):
        index = 0
        books = list()
        while index < len(book_id_list):
            books += Bookinfo.objects.filter(
                szbookid__in=book_id_list[index:index+2000])
            index += 2000

        return books


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
        return trans_case_no(self.szbookcaseno)

    @staticmethod
    def get_cases_by_catalog(catalog_prefix):
        cases = Bookcaseidinfo.objects.all()
        cases = Bookcaseidinfo.objects.exclude(szfirstbookid__isnull=True)
        cases = cases.exclude(szfirstbookid__exact='')
        cases = cases.filter(szpretendindexnum__startswith=catalog_prefix)
        cases = cases.order_by('szpretendindexnum')

        return cases

    @staticmethod
    def get_cases_by_area(area_prefix):
        area = "%06d" % area_prefix
        cases = Bookcaseidinfo.objects.exclude(szfirstbookid__isnull=True)
        cases = cases.exclude(szfirstbookid__exact='')
        cases = cases.filter(szbookcaseno__startswith=area)
        cases = cases.order_by('szpretendindexnum')

        return cases
