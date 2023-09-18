from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font


def Upload(list_new, list_ident = None, list_remove = None):
    # создание нового файла
    wb = Workbook()
    ws = wb.active
    
    #название листа
    ws.title = "Сравнение"
        
    #получаем заголовки столбиков в список
    list_members = []
    if list_ident==None:
        list_members = list_new.__dict__()
    else:
        list_members = list(set(list_new.__dict__()).intersection(list_ident.__dict__()).intersection(list_remove.__dict__()))
     
    #удаляем спец. поля класса
    for var in list_members:
        if var[:2]=="__":
            list_members.remove(var)
    
    #меняем заголовки столбиков
    for index, val in enumerate(list_members):
        ws.cell(row=1, column=index+1).value = val
        ws.cell(row=1, column=index+1).font = Font(size=15, bold=True)

    #добавляем новые элементы
    temp_row = 2
    for i in range(len(list_new)):
        ws[f"A{temp_row}"].value = list_new[i][0]
        ws[f"B{temp_row}"].value = list_new[i][1]
        ws[f"C{temp_row}"].value = list_new[i][2]
        ws[f"D{temp_row}"].value = list_new[i][3]
        ws[f"A{temp_row}"].fill = PatternFill(fill_type='solid', start_color='00FF00', end_color='00FF00')
        ws[f"B{temp_row}"].fill = PatternFill(fill_type='solid', start_color='00FF00', end_color='00FF00')
        ws[f"C{temp_row}"].fill = PatternFill(fill_type='solid', start_color='00FF00', end_color='00FF00')
        ws[f"D{temp_row}"].fill = PatternFill(fill_type='solid', start_color='00FF00', end_color='00FF00')
        temp_row += 1
    
    if list_ident != None:
        #добавляем одинаковые элементы
        for i in range(len(list_ident)):
            ws[f"A{temp_row}"].value = list_ident[i][0]
            ws[f"B{temp_row}"].value = list_ident[i][1]
            ws[f"C{temp_row}"].value = list_ident[i][2]
            ws[f"D{temp_row}"].value = list_ident[i][3]
            temp_row += 1
        
        #добавляем удалённые элементы
        for i in range(len(list_remove)):
            ws[f"A{temp_row}"].value = list_remove[i][0]
            ws[f"B{temp_row}"].value = list_remove[i][1]
            ws[f"C{temp_row}"].value = list_remove[i][2]
            ws[f"D{temp_row}"].value = list_remove[i][3]
            ws[f"A{temp_row}"].fill = PatternFill(fill_type='solid', start_color='FF0000', end_color='FF0000')
            ws[f"B{temp_row}"].fill = PatternFill(fill_type='solid', start_color='FF0000', end_color='FF0000')
            ws[f"C{temp_row}"].fill = PatternFill(fill_type='solid', start_color='FF0000', end_color='FF0000')
            ws[f"D{temp_row}"].fill = PatternFill(fill_type='solid', start_color='FF0000', end_color='FF0000')
            temp_row += 1

    wb.save('Compare.xlsx')