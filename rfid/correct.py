from models import Bookinfo
from django.utils.dateparse import parse_date
import re


def correct_index():
    books = Bookinfo.objects.filter(dtconvertdate__gt=parse_date("2013-08-27"))
    books = list(books)
    reg = re.compile("^\d+")
    count = 0
    for book in books:
        match = reg.match(book.szbookindex)
        if match:
            before = book.szbookindex
            book.szbookindex = before[match.end():]
            print("%s => %s" % (before, book.szbookindex))
            count += 1
            book.save()
    print("%d/%d" % (count, len(books)))
