from openpyxl import Workbook
from openpyxl.styles import Font


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
    
    #добавляем новые элементы
    temp_row = 2
    for i in range(len(list_new)):
        ws[f"A{temp_row}"].value = list_new[i].author
        ws[f"B{temp_row}"].value = list_new[i].title
        ws[f"C{temp_row}"].value = list_new[i].year
        ws[f"D{temp_row}"].value = list_new[i].link
        ws[f"A{temp_row}"].font = Font(color="00FF00", italic=True)
        ws[f"B{temp_row}"].font = Font(color="00FF00", italic=True)
        ws[f"C{temp_row}"].font = Font(color="00FF00", italic=True)
        ws[f"D{temp_row}"].font = Font(color="00FF00", italic=True)
        temp_row += 1
    
    #добавляем одинаковые элементы
    for i in range(len(list_ident)):
        ws[f"A{temp_row}"].value = list_ident[i].author
        ws[f"B{temp_row}"].value = list_ident[i].title
        ws[f"C{temp_row}"].value = list_ident[i].year
        ws[f"D{temp_row}"].value = list_ident[i].link
        temp_row += 1
        
    #добавляем удалённые элементы
    for i in range(len(list_remove)):
        ws[f"A{temp_row}"].value = list_remove[i].author
        ws[f"B{temp_row}"].value = list_remove[i].title
        ws[f"C{temp_row}"].value = list_remove[i].year
        ws[f"D{temp_row}"].value = list_remove[i].link
        ws[f"A{temp_row}"].font = Font(color="FF0000", italic=True)
        ws[f"B{temp_row}"].font = Font(color="FF0000", italic=True)
        ws[f"C{temp_row}"].font = Font(color="FF0000", italic=True)
        ws[f"D{temp_row}"].font = Font(color="FF0000", italic=True)
        temp_row += 1

    wb.save('Compare.xlsx')