from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font


def Upload(list_new, list_ident, list_remove):
    # создание нового файла
    wb = Workbook()
    ws = wb.active
    
    #название листа
    ws.title = "Сравнение"
    
    #меняем заголовки столбиков
    ws["A1"].value = "Author"
    ws["B1"].value = "Title"
    ws["C1"].value = "Year"
    ws["D1"].value = "Link"   
    
    ws["A1"].font = Font(size=15, bold=True)
    ws["B1"].font = Font(size=15, bold=True)
    ws["C1"].font = Font(size=15, bold=True)
    ws["D1"].font = Font(size=15, bold=True)

    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 130
    ws.column_dimensions['C'].width = 10
    ws.column_dimensions['D'].width = 150

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