import json
import xmltodict
from App import Translite
from App import eLibrary_Library
from App import clear_author


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
    for e in list_library:
        #try:    
            count_author_temp = 0
            #список авторов
            list_author = e["authors"]["author"]
        
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
                except:
                    new_article.author = new_article.original_author
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
                        except:
                            new_article.author = new_article.original_author
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
                if "titles" in e:
                    if "title" in e["titles"]:
                        #если одно название:
                        if type(e["titles"]["title"])==dict:    
                            if "#text" in e["titles"]["title"]:
                                    all_elibrary_list_library[i].title = e["titles"]["title"]["#text"]
                        #если несколько названий
                        else:
                            if type(e["titles"]["title"])==list:
                                for t in e["titles"]["title"]:
                                    if t["@lang"]=="EN":
                                        all_elibrary_list_library[i].title = t["#text"]
                                        break
                all_elibrary_list_library[i].title = all_elibrary_list_library[i].title.lower()
                all_elibrary_list_library[i].title = all_elibrary_list_library[i].title[0].upper() + all_elibrary_list_library[i].title[1:]
                                    
                #год
                if "source" in e:
                    if "issue" in e["source"]:
                        if "year" in e["source"]["issue"]:
                            all_elibrary_list_library[i].year = e["source"]["issue"]["year"]
                if all_elibrary_list_library[i].year == None or all_elibrary_list_library[i].year == "":
                    if "yearpubl" in e:
                        all_elibrary_list_library[i].year = e["yearpubl"]
                if all_elibrary_list_library[i].year == None:
                    all_elibrary_list_library[i].year = ""
                    
                #ссылка
                if "linkurl" in e:
                    all_elibrary_list_library[i].link = e["linkurl"]
                
                #doi
                if "doi" in e:
                    all_elibrary_list_library[i].doi = e["doi"]
                    
                #id
                if "@id" in e:
                    all_elibrary_list_library[i].id = e["@id"]
                
                #type
                if "type" in e:
                    all_elibrary_list_library[i].type = e["type"]
                
                #citation
                if "cited" in e:
                    all_elibrary_list_library[i].citation = e["cited"]
            
                #pages
                if "pages" in e:
                    all_elibrary_list_library[i].pages = e["pages"]
                
                #volume
                if "source" in e:
                    if "issue" in e["source"]:
                        if "volume" in e["source"]["issue"]:
                            all_elibrary_list_library[i].volume = e["source"]["issue"]["volume"]
                        
                #issn
                if "source" in e:
                    if "journal" in e["source"]:
                        if "issn" in e["source"]["journal"]:
                            all_elibrary_list_library[i].issn = e["source"]["journal"]["issn"]
                        
                #eissn
                if "source" in e:
                    if "journal" in e["source"]:
                        if "eissn" in e["source"]["journal"]:
                            all_elibrary_list_library[i].eissn = e["source"]["journal"]["eissn"]
                        
                #title_journal
                if "source" in e:
                    if "journal" in e["source"]:
                        if "title" in e["source"]["journal"]:
                            all_elibrary_list_library[i].title_journal = e["source"]["journal"]["title"]
                        
                #publisher
                if "source" in e:
                    if "journal" in e["source"]:
                        if "publisher" in e["source"]["journal"]:
                            all_elibrary_list_library[i].publisher = e["source"]["journal"]["publisher"]
                        
                #country
                if "source" in e:
                    if "journal" in e["source"]:
                        if "country" in e["source"]["journal"]:
                            all_elibrary_list_library[i].country = e["source"]["journal"]["country"]
                        
                #GRNTI_code
                if "grnti" in e:
                    all_elibrary_list_library[i].GRNTI_code = e["grnti"]
                            
            count_all_author += count_author_temp
        # except:
        #     pass
        
    for i in range(len(all_elibrary_list_library)):
        all_elibrary_list_library[i].clear_title = "".join(e for e in all_elibrary_list_library[i].title.lower() if e.isalpha())
        
    for i in range(len(all_elibrary_list_library)):
        all_elibrary_list_library[i].clear_author = "".join(e for e in all_elibrary_list_library[i].author if e.isupper())
    
    return all_elibrary_list_library