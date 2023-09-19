from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font


def Upload(path, list_new, list_ident = None, list_remove = None):
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
        for j in range(1, len(list_members)+1):
            x = getattr(list_new[i], list_members[j])
            ws.cell(row=i+temp_row, column=j).value = x
            if list_ident == None:
                ws.cell(row=i+temp_row, column=j).fill = PatternFill(fill_type='solid', start_color='00FF00', end_color='00FF00')
    temp_row += len(list_new)

    #добавляем поля из других, если они существуют
    if list_ident != None:
        #добавляем одинаковые элементы
        for i in range(len(list_new)):
            for j in range(1, len(list_members)+1):
                x = getattr(list_new[i], list_members[j])
                ws.cell(row=i+temp_row, column=j).value = x
                if list_ident == None:
                    ws.cell(row=i+temp_row, column=j).fill = PatternFill(fill_type='solid', start_color='00FF00', end_color='00FF00')
        temp_row += len(list_new)
        
        #добавляем удалённые элементы
        for i in range(len(list_new)):
            for j in range(1, len(list_members)+1):
                x = getattr(list_new[i], list_members[j])
                ws.cell(row=i+temp_row, column=j).value = x
                if list_ident == None:
                    ws.cell(row=i+temp_row, column=j).fill = PatternFill(fill_type='solid', start_color='00FF00', end_color='00FF00')
        temp_row += len(list_new)

    wb.save('Compare.xlsx')
    #wb.save(path)