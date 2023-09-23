from openpyxl import load_workbook
from Class import IPublishing_Library
from Translate import Translite
from clear_str import clear_str


def IPublishing(path):
    # список статей IPublishing
    all_IPublishing_list_library = []

    # открытие исходного файла с проверкой 
    try:
        wb = load_workbook(path)
        ws = wb.active
    except:
        return None

    try:
        # ПАРСИНГ КАЖДОЙ СТРОКИ
        for row_index in range(5, ws.max_row + 1):
            str_author = ws[f"G{row_index}"].value #строка с авторами 
            list_author = str_author.split(",") #список авторов
            for i in range (len(list_author)):
                new_author = IPublishing_Library()
            
                new_author.author_rus = list_author[i].strip()
            
                if ws[f"H{row_index}"].value != None:
                    new_author.title = ws[f"H{row_index}"].value
            
                if ws[f"E{row_index}"].value != None:
                    new_author.year = ws[f"E{row_index}"].value
            
                if ws[f"I{row_index}"].value != None:
                    new_author.article = ws[f"I{row_index}"].value
            
                if ws[f"AF{row_index}"].value != None:
                    new_author.link = ws[f"AF{row_index}"].value
            
                if ws[f"J{row_index}"].value != None:
                    new_author.description = ws[f"J{row_index}"].value
            
                if ws[f"AG{row_index}"].value != None:
                    new_author.doi = ws[f"AG{row_index}"].value
            
                if ws[f"B{row_index}"].value != None:
                    new_author.institute = ws[f"B{row_index}"].value
            
                if ws[f"C{row_index}"].value != None:
                    new_author.faculty = ws[f"C{row_index}"].value
            
                if ws[f"D{row_index}"].value != None:
                    new_author.cathedra = ws[f"D{row_index}"].value
                
                if ws[f"J{row_index}"].value != None:
                    new_author.full_bibliographic_description = ws[f"J{row_index}"].value
                
                if ws[f"V{row_index}"].value != None:
                    new_author.cod_OECD = ws[f"V{row_index}"].value
                
                if ws[f"W{row_index}"].value != None:
                    new_author.group_of_scientific_specialties = ws[f"W{row_index}"].value
                
                if ws[f"X{row_index}"].value != None:
                    new_author.GRNTI_code = ws[f"X{row_index}"].value
                
                if ws[f"Y{row_index}"].value != None:
                    new_author.quartile_wos = ws[f"Y{row_index}"].value
                
                if ws[f"Z{row_index}"].value != None:
                    new_author.quartile_scopus = ws[f"Z{row_index}"].value
                
                if ws[f"AA{row_index}"].value != None:
                    new_author.quartile_scopus_sjr = ws[f"AA{row_index}"].value
                
                if ws[f"AB{row_index}"].value != None:
                    new_author.impact_factor_wos = ws[f"AB{row_index}"].value
                
                if ws[f"AC{row_index}"].value != None:
                    new_author.impact_factor_scopus = ws[f"AC{row_index}"].value
                    
                if ws[f"AD{row_index}"].value != None:
                    new_author.impact_factor_elibrary_5_year = ws[f"AD{row_index}"].value
                
                if ws[f"AE{row_index}"].value != None:
                    new_author.impact_factor_elibrary_2_year = ws[f"AE{row_index}"].value
    
            all_IPublishing_list_library.append(new_author)
    except:
        return None

    for i in range(len(all_IPublishing_list_library)):
        all_IPublishing_list_library[i].author = Translite(all_IPublishing_list_library[i].author_rus)
        new = all_IPublishing_list_library[i].author.split()
        if len(new)==3:
            new[1] = f"{new[1][0]}"
            if new[2][0]==".":
                new[2] = f"{new[2][1]}"
            else:
                new[2] = f"{new[2][0]}"
            all_IPublishing_list_library[i].author = f"{new[0]} {new[1]}.{new[2]}."
        if len(new)==2:
            counter = new[1].count('.')
            if counter==2:
                new_str_1 = f"{new[1][0]}"
                ii = 1
                while new[1][ii]!=".":
                    ii += 1
                ii += 1
                new_str_2 = f"{new[1][ii]}"
                all_IPublishing_list_library[i].author = f"{new[0]} {new_str_1}.{new_str_2}."
            else:
                all_IPublishing_list_library[i].author = f"{new[0]} {new[1][0]}."
                
        all_IPublishing_list_library[i].author = clear_str(all_IPublishing_list_library[i].author)
        
    for i in range(len(all_IPublishing_list_library)):
        all_IPublishing_list_library[i].clear_title = "".join(e for e in all_IPublishing_list_library[i].title.lower() if e.isalpha())
        
    for i in range(len(all_IPublishing_list_library)):
        all_IPublishing_list_library[i].clear_author = "".join(e for e in all_IPublishing_list_library[i].author if e.isupper())
        
    return all_IPublishing_list_library
