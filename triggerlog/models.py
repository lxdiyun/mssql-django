from django.db import models
from utils import trans_case_no
from re import search


class TriggerLog(models.Model):
    appname = models.TextField(db_column='AppName', blank=True)
    username = models.TextField(db_column='UserName', blank=True)
    sql = models.TextField(db_column='Sql', blank=True)
    hostname = models.TextField(db_column='HostName', blank=True)
    time = models.DateTimeField(null=True, db_column='Time', blank=True)
    tablename = models.TextField(blank=True)
    state = models.TextField(blank=True)
    object = models.TextField(blank=True)
    before = models.TextField(blank=True)
    after = models.TextField(blank=True)

    class Meta:
        db_table = 'trigger_log'

    def get_case_no(self):
        return self.state[:14]

    def get_before(self):
        s = search("before:(\d+),", self.state)
        return s.group(1)

    def get_after(self):
        s = search("after:(\d+)", self.state)
        return s.group(1)

    def translate_case_no(self):
        return trans_case_no(self.get_case_no())
