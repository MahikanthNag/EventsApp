import urllib
import os, django
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled9.settings")

application = get_wsgi_application()

from Events.models import *
import click
from  openpyxl import load_workbook
import MySQLdb
from  BeautifulSoup import BeautifulSoup
@click.group()
def cli():
    pass

@cli.command()
@click.argument('xlsxfile1',nargs=1)

def populatedata(xlsxfile1):
    wb=load_workbook(xlsxfile1)

    rows=wb.get_sheet_by_name('Sheet1'.title()).rows
    for row in rows:
        print row[0].value
        print row[1].value
        username = row[0].value.split('@')[0]
        tl=User(username = username, first_name=row[1].value,email=row[0].value, password="password")
        tl.save()
if __name__=='__main__':
    cli()
