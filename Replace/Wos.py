from openpyxl import load_workbook
from Class import WOS_Library

def Wos(path):
    #�������� ��������� �����
    wb = load_workbook(path)
    ws = wb.active
    
    #������ ������ SCOPUS
    all_wos_list_library = []

    #���-�� ��� �������
    count_all_author = 0
    
    #������� ������ ������
    for row in ws.iter_rows(min_row=2, values_only=True):
        pass