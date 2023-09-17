from openpyxl import Workbook
from openpyxl.styles import PatternFill


def Upload(list_new, list_ident, list_remove):
    # создание нового файла
    wb = Workbook()
    ws = wb.active
    
    #название листа
    ws.title = "Сравнение"
    
    #меняем заголовки столбиков
    ws["A1"].value = "author"
    ws["B1"].value = "title"
    ws["C1"].value = "year"
    ws["D1"].value = "link"
    
    #цвет
    colors = ['0000FF00', '00660066']
    fillers = []
    for color in colors:
        temp = PatternFill(patternType='solid',fgColor=color)
        fillers.append(temp)
    
    #добавляем новые элементы
    temp_row = 1
    for i in range(len(list_new)):
        ws[f"A{i}"].value = list_new[i].author
        ws[f"B{i}"].value = list_new[i].title
        ws[f"C{i}"].value = list_new[i].year
        ws[f"D{i}"].value = list_new[i].link
        ws[f"A{i}"].fill = fillers[1]
        ws[f"B{i}"].fill = fillers[1]
        ws[f"C{i}"].fill = fillers[1]
        ws[f"D{i}"].fill = fillers[1]
        temp_row += 1
    
    #добавляем одинаковые элементы
    for i in range(len(list_ident)):
        ws[f"A{i}"].value = list_ident[i].author
        ws[f"B{i}"].value = list_ident[i].title
        ws[f"C{i}"].value = list_ident[i].year
        ws[f"D{i}"].value = list_ident[i].link
        temp_row += 1
        
    #добавляем удалённые элементы
    for i in range(len(list_ident)):
        ws[f"A{i}"].value = list_remove[i].author
        ws[f"B{i}"].value = list_remove[i].title
        ws[f"C{i}"].value = list_remove[i].year
        ws[f"D{i}"].value = list_remove[i].link
        ws[f"A{i}"].fill = fillers[0]
        ws[f"B{i}"].fill = fillers[0]
        ws[f"C{i}"].fill = fillers[0]
        ws[f"D{i}"].fill = fillers[0]
        temp_row += 1

    wb.save('Compare.xlsx')