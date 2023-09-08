from openpyxl import Workbook, load_workbook
from Class import IPublishing_Library

def IPublishing(path):
    #открытие исходного файла
    wb = load_workbook(path)
    wb.active = wb['1. Статьи в журналах']
    wb.active = wb['1. Статьи в журналах']
    ws = wb.active
    print(ws.title)