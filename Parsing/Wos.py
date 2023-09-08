from openpyxl import load_workbook
from Class import WOS_Library

def Wos(path):
    #открытие исходного файла
    wb = load_workbook(path)
    ws = wb.active
    
    #список статей SCOPUS
    all_wos_list_library = []
    
    #ПАРСИНГ КАЖДОЙ СТРОКИ
    for row_index in range(2, ws.max_row+1):
        new_author = WOS_Library()
        new_author.author = ws[f"F{row_index}"].value
        new_author.title = ws[f"I{row_index}"].value
        new_author.year = ws[f"AU{row_index}"].value
        new_author.volume = ws[f"AV{row_index}"].value
        new_author.issue = ws[f"AW{row_index}"].value
        new_author.article = ws[f"BD{row_index}"].value
        new_author.start_page = ws[f"BB{row_index}"].value
        new_author.end_page = ws[f"BC{row_index}"].value
        new_author.number_of_pages = ws[f"AX{row_index}"].value
        new_author.doi = ws[f"BE{row_index}"].value
        if ws[f"BF{row_index}"].value!=None:
            new_author.link = ws[f"BF{row_index}"].value[10:]
        all_wos_list_library.append(new_author)

    #вывод в файл
    print("Запись в файл началась")        
    with open("Source/Wos/Result.txt", "w",encoding="utf-8") as file:
        for index, val in enumerate(all_wos_list_library):
            file.write("Запись №: "+str(index)+"\n")
            file.write(val.Print())
            file.write("\n\n\n")
    print("Всего строк: " + str(ws.max_row))
    return all_wos_list_library