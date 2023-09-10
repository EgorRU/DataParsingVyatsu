from openpyxl import load_workbook
from Class import IPublishing_Library


def IPublishing(path):
    # открытие исходного файла
    wb = load_workbook(path)
    wb.active = wb["1. Статьи в журналах"]
    ws = wb.active

    # список статей IPublishing
    all_IPublishing_list_library = []

    # ПАРСИНГ КАЖДОЙ СТРОКИ
    for row_index in range(5, ws.max_row + 1):
        str_author = ws[f"G{row_index}"].value #строка с авторами 
        list_author = str_author.split(",") #список авторов
        for i in range (len(list_author)):
            new_author = IPublishing_Library()
            new_author.author = list_author[i].strip()
            new_author.title = ws[f"I{row_index}"].value
            new_author.year = ws[f"E{row_index}"].value
            new_author.article = ws[f"H{row_index}"].value
            new_author.link = ws[f"AF{row_index}"].value
            new_author.description = ws[f"J{row_index}"].value
            new_author.doi = ws[f"AG{row_index}"].value
            all_IPublishing_list_library.append(new_author)

    # вывод в файл
    print("Запись в файл началась IPublishing")
    print(f"Всего строк в таблице: {ws.max_row-4}")
    print(f"Всего записей: {len(all_IPublishing_list_library)}")
    print("---------------------------------------")
    with open("Source/IPublishing/Result.txt", "w", encoding="utf-8") as file:
        for index, val in enumerate(all_IPublishing_list_library):
            file.write("Запись №: " + str(index) + "\n")
            file.write(val.Print())
            file.write("\n\n\n")
    return all_IPublishing_list_library
