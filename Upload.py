from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Border, Side


def Upload(path, list_new = [], list_ident = [], list_remove = []):
    # создание нового файла
    wb = Workbook()
    ws = wb.active
    
    #границы ячейки
    border=Border(top=Side(border_style='thick',color="A52A2A"))

    #название листа 
    ws.title = "Сравнение данных"
        
    #получаем заголовки столбиков в список
    list_members = []
    if len(list_new)>0:
        list_members = list_new[0].__dir__()
        if len(list_ident)>0:
            list_members = list(set(list_members).intersection(set(list_ident[0].__dir__())))
        if len(list_remove)>0:
            list_members = list(set(list_members).intersection(set(list_remove[0].__dir__()))) 
    else:
        if len(list_ident)>0:
            list_members = list_ident[0].__dir__()
            if len(list_remove)>0:
                list_members = list(set(list_members).intersection(set(list_remove[0].__dir__()))) 
        else:
            if len(list_remove)>0:
                list_members = list_remove[0].__dir__()
    
    #удаляем спец. поля класса
    new_list_members = []       
    for var in list_members:
        if var[0] != "_" and var[0].islower() and var[:5]!="clear":
            new_list_members.append(var)
            
    #формируем сортированный список
    new_list_members.remove("author")
    new_list_members.remove("title")
    new_list_members.remove("year")
    list_members = ["№ article","author","title","year", "full bibliographic title"]
    
    #если есть поля, то добавляем в нужной очерёдности
    if "doi" in new_list_members:
        list_members.append("doi")
        new_list_members.remove("doi")
        
    if "link" in new_list_members:
        list_members.append("link")
        new_list_members.remove("link")
        
    if "start_page" in new_list_members:
        list_members.append("start_page")
        new_list_members.remove("start_page")
        
    if "end_page" in new_list_members:
        list_members.append("end_page")
        new_list_members.remove("end_page")
        
    if "issue" in new_list_members:
        list_members.append("issue")
        new_list_members.remove("issue")
    
    if "volume" in new_list_members:
        list_members.append("volume")
        new_list_members.remove("volume")
        
    if "article" in new_list_members:
        list_members.append("article")
        new_list_members.remove("article")
        
    if "citation" in new_list_members:
        list_members.append("citation")
        new_list_members.remove("citation")
        
    #добавляем остальные поля
    for i in range(len(new_list_members)):
        list_members.append(new_list_members[i])
    
    for i in range (len(list_members)):
        print(list_members[i])

    #меняем заголовки столбиков
    for index, val in enumerate(list_members):
        ws.cell(row=1, column=index+1).value = val
        ws.cell(row=1, column=index+1).font = Font(size=16)
    
    #меняем ширину ячеек
    for i in range(len(list_members)):
        ws.column_dimensions[ws.cell(row=1, column=i+1).column_letter].width = 30
    ws.column_dimensions["A"].width = 10
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 70
    ws.column_dimensions["D"].width = 10
    ws.column_dimensions["E"].width = 80
      
    #если выгружаем больше одного листа
    temp_row = 2
    count_article = 0
    
    #добавляем новые элементы
    title = ""
    for i in range(len(list_new)):
        title_temp = getattr(list_new[i], "title")
        ws.cell(row=i+temp_row, column=1).font = Font(size=16)
        ws.cell(row=i+temp_row, column=1).fill = PatternFill(fill_type='solid', start_color='7FFF00', end_color='7FFF00')
        if title_temp!= title:
            ws.cell(row=i+temp_row, column=1).border = border
            count_article += 1
            for j in range(1, len(list_members)):
                if j==4:
                    ws.cell(row=i+temp_row, column=j+1).value = "test"
                else:
                    ws.cell(row=i+temp_row, column=j+1).value = getattr(list_new[i], list_members[j])
                ws.cell(row=i+temp_row, column=j+1).border = border
                ws.cell(row=i+temp_row, column=j+1).fill = PatternFill(fill_type='solid', start_color='7FFF00', end_color='7FFF00')
        else:
            for j in range(1, len(list_members)):
                if j==4:
                    ws.cell(row=i+temp_row, column=j+1).value = "test"
                else:
                    ws.cell(row=i+temp_row, column=j+1).value = getattr(list_new[i], list_members[j])
                ws.cell(row=i+temp_row, column=j+1).fill = PatternFill(fill_type='solid', start_color='7FFF00', end_color='7FFF00')
        ws.cell(row=i+temp_row, column=1).value = count_article
        title = title_temp
    temp_row += len(list_new)


    #добавляем одинаковые элементы
    title = ""
    for i in range(len(list_ident)):
        title_temp = getattr(list_ident[i], "title")
        ws.cell(row=i+temp_row, column=1).font = Font(size=16)
        if title_temp!= title:
            ws.cell(row=i+temp_row, column=1).border = border
            count_article += 1              
            for j in range(1, len(list_members)):
                if j==4:
                    ws.cell(row=i+temp_row, column=j+1).value = "test"
                else:
                    ws.cell(row=i+temp_row, column=j+1).value = getattr(list_ident[i], list_members[j]) 
                ws.cell(row=i+temp_row, column=j+1).border  = border
        else:
            for j in range(1, len(list_members)):
                if j==4:
                    ws.cell(row=i+temp_row, column=j+1).value = "test"
                else:
                    ws.cell(row=i+temp_row, column=j+1).value = getattr(list_ident[i], list_members[j])  
        ws.cell(row=i+temp_row, column=1).value = count_article
        title = title_temp
    temp_row += len(list_ident)
        

    #добавляем удалённые элементы
    title = ""
    for i in range(len(list_remove)):
        title_temp = getattr(list_remove[i], "title")
        ws.cell(row=i+temp_row, column=1).font = Font(size=16)
        ws.cell(row=i+temp_row, column=1).fill = PatternFill(fill_type='solid', start_color='F08080', end_color='F08080')
        if title_temp!= title:
            ws.cell(row=i+temp_row, column=1).border = border
            count_article += 1
            for j in range(1, len(list_members)):
                if j==4:
                    ws.cell(row=i+temp_row, column=j+1).value = "test"
                else:
                    ws.cell(row=i+temp_row, column=j+1).value = getattr(list_remove[i], list_members[j])
                ws.cell(row=i+temp_row, column=j+1).fill = PatternFill(fill_type='solid', start_color='F08080', end_color='F08080')
                ws.cell(row=i+temp_row, column=j+1).border  = border
        else:
            for j in range(1, len(list_members)):
                if j==4:
                    ws.cell(row=i+temp_row, column=j+1).value = "test"
                else:
                    ws.cell(row=i+temp_row, column=j+1).value = getattr(list_remove[i], list_members[j])
                ws.cell(row=i+temp_row, column=j+1).fill = PatternFill(fill_type='solid', start_color='F08080', end_color='F08080')
        ws.cell(row=i+temp_row, column=1).value = count_article
        title = title_temp
    temp_row += len(list_remove)
             
    print(f"Для проверки: {len(list_new)+len(list_ident)+len(list_remove)} = {ws.max_row-1}")
    wb.save(path)
