from openpyxl import load_workbook
from Class import WOS_Library


def Wos(path):
    # список статей Wos
    all_wos_list_library = []

    # открытие исходного файла
    wb = load_workbook(path)
    ws = wb.active

    #проверка на то, что открыли
    if ws.cell(row=1, column=1).value.strip()[:6] == "Авторы":
        return all_wos_list_library, "Scopus"

    if ws.cell(row=1, column=1).value.strip()[:7] == "Таблица":
        return all_wos_list_library, "IPublishing"

    # ПАРСИНГ КАЖДОЙ СТРОКИ
    for row_index in range(2, ws.max_row + 1):
        str_author = ws[f"F{row_index}"].value #строка с авторами 
        str_author = str_author.replace(",","") #убираем запятые
        list_author = str_author.split(";") #список авторов
        for i in range (len(list_author)):
            new_author = WOS_Library()
            new_author.author = list_author[i].strip()
            if ws[f"I{row_index}"].value != None:
                new_author.title = ws[f"I{row_index}"].value.lower()
                new_author.title = new_author.title[0].upper() + new_author.title[1:]
            new_author.year = ws[f"AU{row_index}"].value
            new_author.volume = ws[f"AV{row_index}"].value
            new_author.issue = ws[f"AW{row_index}"].value
            if ws[f"BD{row_index}"].value != None:
                new_author.article = str(ws[f"BD{row_index}"].value).lower()
                new_author.article = new_author.article[0].upper() + new_author.article[1:]
            new_author.start_page = ws[f"BB{row_index}"].value
            new_author.end_page = ws[f"BC{row_index}"].value
            new_author.number_of_pages = ws[f"AX{row_index}"].value
            new_author.doi = ws[f"BE{row_index}"].value
            if ws[f"BF{row_index}"].value != None:
                new_author.link = ws[f"BF{row_index}"].value[10:].strip()
            all_wos_list_library.append(new_author)


    for i in range(len(all_wos_list_library)):
        all_wos_list_library[i].clear_title = "".join(e for e in all_wos_list_library[i].title.lower() if e.isalpha())
        
    for i in range(len(all_wos_list_library)):
        all_wos_list_library[i].clear_author = "".join(e for e in all_wos_list_library[i].author if e.isupper())
        
    # вывод в файл
    print("Запись в файл началась Wos")
    print(f"Всего строк в таблице: {ws.max_row-1}")
    print(f"Всего записей: {len(all_wos_list_library)}")
    print("---------------------------------------")
    with open("Source/Wos/Result.txt", "w", encoding="utf-8") as file:
        for index, val in enumerate(all_wos_list_library):
            file.write("Запись №: " + str(index) + "\n")
            file.write(val.Print())
            file.write("\n\n\n")
    return all_wos_list_library, "Wos"
