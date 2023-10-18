import json
import xmltodict
import re
from App import Translite
from App import eLibrary_Library
from App import clear_author
from Logging import writeFile


def eLibrary(path):
    # список статей eLibrary
    all_elibrary_list_library = []

    #проверка на то, что открыли
    if path[-3:]!="xml":
        return None

    #читаем исходный xml и убираем проблемный символ
    file = open(path, 'br')
    s = ""
    symbol = s.encode("utf-8")
    data = file.read()
    data = data.replace(symbol, b"")
    file.close()
    
    #перезаписываем xml файл
    file = open(path, 'bw')
    file.write(data)
    file.close()

    #читаем заново и делаем json словарь
    file = open(path, "r", encoding="utf-8")
    data = file.read()
    dict_data = xmltodict.parse(data)
    file.close()
    
    #записываем словарь в файл
    with open("eLibrary.json", 'w', encoding="utf-8") as file:
        json.dump(dict_data, file, ensure_ascii=False, indent=4)

    #читаем словарь json
    file = open('eLibrary.json', 'r', encoding="utf-8")
    dict_data = json.load(file)
    file.close()

    #парсим json словарь
    count_all_author = 0
    list_library = dict_data["items"]["item"]
    
    #по каждой записи
    for lib in list_library:
        try:    
            count_author_temp = 0
            #список авторов
            list_author = lib["authors"]["author"]
            #если автор один
            if type(list_author)==dict:
                new_article = eLibrary_Library()
                if "lastname" in list_author:
                    new_article.author = str(list_author["lastname"])
                if "initials" in list_author:
                    new_article.author = new_article.author + " " + str(list_author["initials"])
                if new_article.author != None:
                    new_article.original_author = new_article.author.strip()
                try:
                    new_article.author = clear_author(Translite(clear_author(new_article.original_author)))
                except Exception as e: 
                    writeFile("exception", f"{str(e)}\n")
                    writeFile("info", f"Сломанный автор в ели: {new_article.original_author}\n")
                    new_article.author = new_article.original_author
                new_article.author = new_article.author.replace("Bajkova", "Baykova")
                count_author_temp += 1
                all_elibrary_list_library.append(new_article)
            #если авторов много
            else:
                if type(list_author)==list:
                    #создаём экземпляры
                    old_article = ""
                    for auth in list_author:
                        #создаём запись
                        new_article = eLibrary_Library()
                        if "lastname" in auth:
                            new_article.author = str(auth["lastname"])
                        if "initials" in auth:
                            new_article.author = new_article.author + " " + str(auth["initials"])
                        if new_article.author != None:
                            new_article.original_author = new_article.author.strip()
                        try:
                            new_article.author = clear_author(Translite(clear_author(new_article.original_author)))
                        except Exception as e: 
                            writeFile("exception", f"{str(e)}\n")
                            writeFile("info", f"Сломанный автор в ели: {new_article.original_author}\n")
                            new_article.author = new_article.original_author
                        new_article.author = new_article.author.replace("Bajkova", "Baykova")
                        #если запись не повторяется
                        if old_article=="":
                            all_elibrary_list_library.append(new_article)
                            count_author_temp += 1
                        else:
                            if new_article.author != old_article.author:
                                all_elibrary_list_library.append(new_article)
                                count_author_temp += 1
                        #заменяем прошлую запись для дальнейшего сравнения
                        old_article = new_article
                

            #по всем новым авторам добавляем новые поля
            for i in range(count_all_author, count_all_author + count_author_temp):
                #название
                if "titles" in lib:
                    if "title" in lib["titles"]:
                        #если одно название:
                        if type(lib["titles"]["title"])==dict:    
                            if "#text" in lib["titles"]["title"]:
                                    all_elibrary_list_library[i].title = re.sub(r'\<[^>]*\>', "", lib["titles"]["title"]["#text"])
                        #если несколько названий
                        else:
                            if type(lib["titles"]["title"])==list:
                                for t in lib["titles"]["title"]:
                                    if t["@lang"]=="RU":
                                        all_elibrary_list_library[i].title = re.sub(r'\<[^>]*\>', "", t["#text"])
                                        break
                                else:
                                    for t in lib["titles"]["title"]:
                                        if t["@lang"]=="EN":
                                            all_elibrary_list_library[i].title = re.sub(r'\<[^>]*\>', "", t["#text"])
                                            break
                all_elibrary_list_library[i].title = all_elibrary_list_library[i].title.lower()
                all_elibrary_list_library[i].title = all_elibrary_list_library[i].title[0].upper() + all_elibrary_list_library[i].title[1:]
                                    
                #год
                if "source" in lib:
                    if "issue" in lib["source"]:
                        if "year" in lib["source"]["issue"]:
                            all_elibrary_list_library[i].year = lib["source"]["issue"]["year"]
                        if "number" in lib["source"]["issue"]:
                            all_elibrary_list_library[i].number = lib["source"]["issue"]["number"] 
                if all_elibrary_list_library[i].year == None or all_elibrary_list_library[i].year == "":
                    if "yearpubl" in lib:
                        all_elibrary_list_library[i].year = lib["yearpubl"]
                if all_elibrary_list_library[i].year == None:
                    all_elibrary_list_library[i].year = ""
                    
                #ссылка
                if "linkurl" in lib:
                    all_elibrary_list_library[i].link = lib["linkurl"]
                
                #doi
                if "doi" in lib:
                    all_elibrary_list_library[i].doi = lib["doi"]
                    
                #id
                if "@id" in lib:
                    all_elibrary_list_library[i].id = lib["@id"]
                
                #type
                if "type" in lib:
                    all_elibrary_list_library[i].type = lib["type"]
                
                #citation
                if "cited" in lib:
                    all_elibrary_list_library[i].citation = lib["cited"]
            
                #pages
                if "pages" in lib:
                    all_elibrary_list_library[i].pages = lib["pages"]
                
                #volume
                if "source" in lib:
                    if "issue" in lib["source"]:
                        if "volume" in lib["source"]["issue"]:
                            all_elibrary_list_library[i].volume = lib["source"]["issue"]["volume"]
                        
                #issn
                if "source" in lib:
                    if "journal" in lib["source"]:
                        if "issn" in lib["source"]["journal"]:
                            all_elibrary_list_library[i].issn = lib["source"]["journal"]["issn"]
                        
                #eissn
                if "source" in lib:
                    if "journal" in lib["source"]:
                        if "eissn" in lib["source"]["journal"]:
                            all_elibrary_list_library[i].eissn = lib["source"]["journal"]["eissn"]
                        
                #title_journal
                if "source" in lib:
                    if "journal" in lib["source"]:
                        if "title" in lib["source"]["journal"]:
                            all_elibrary_list_library[i].title_article = lib["source"]["journal"]["title"]
                if all_elibrary_list_library[i].title_article=="" or all_elibrary_list_library[i].title_article==None:
                    if "source" in lib:
                        if "titleaddinfo" in lib["source"]:
                            all_elibrary_list_library[i].title_article = lib["source"]["titleaddinfo"]
                        if "confname" in lib["source"]:
                            all_elibrary_list_library[i].title_article += f"//{lib['source']['confname']}" 
                        
                #publisher
                if "source" in lib:
                    if "journal" in lib["source"]:
                        if "publisher" in lib["source"]["journal"]:
                            all_elibrary_list_library[i].publisher = lib["source"]["journal"]["publisher"]
                        
                #country
                if "source" in lib:
                    if "journal" in lib["source"]:
                        if "country" in lib["source"]["journal"]:
                            all_elibrary_list_library[i].country = lib["source"]["journal"]["country"]
                        
                #GRNTI_code
                if "grnti" in lib:
                    all_elibrary_list_library[i].GRNTI_code = lib["grnti"]
                            
            count_all_author += count_author_temp
        except Exception as e: 
            writeFile("exception", f"{str(e)}\n")
            writeFile("info", f"Сломанная строка в ели: {json.dump(lib, indent = 4)}\n")
        
    for i in range(len(all_elibrary_list_library)):
        all_elibrary_list_library[i].clear_title = "".join(lib for lib in all_elibrary_list_library[i].title.lower() if lib.isalpha())
        all_elibrary_list_library[i].clear_author = "".join(lib for lib in all_elibrary_list_library[i].author if lib.isupper())
        all_elibrary_list_library[i].title = all_elibrary_list_library[i].title.replace('ё', 'е')
        
    return all_elibrary_list_library