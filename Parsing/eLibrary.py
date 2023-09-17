import json
import xmltodict
from Parsing.Translate import Translite
from Class import eLibrary_Library


def eLibrary(path):
    # список статей eLibrary
    all_elibrary_list_library = []

    #проверка на то, что открыли
    if path[-3:]!="xml":
        return all_elibrary_list_library, ""

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
    with open("Source/eLibrary/eLibrary.json", 'w', encoding="utf-8") as file:
        json.dump(dict_data, file, ensure_ascii=False, indent=4)

    #читаем словарь json
    file = open('Source/eLibrary/eLibrary.json', 'r', encoding="utf-8")
    dict_data = json.load(file)
    file.close()

    #парсим json словарь
    count_all_author = 0
    list_library = dict_data["items"]["item"]
    
    #по каждой записи
    for e in list_library:
        count_author_temp = 0
        #список авторов
        list_author = e["authors"]["author"]
        
        #если автор один
        if type(list_author)==dict:
            new_article = eLibrary_Library()
            if "lastname" in list_author:
                #print(str(auth["lastname"]))
                new_article.author = str(list_author["lastname"])
            if "initials" in list_author:
                    new_article.author = new_article.author + " " + str(list_author["initials"])
            count_author_temp += 1
            all_elibrary_list_library.append(new_article)
        #если авторов много
        else:
            if type(list_author)==list:
                #создаём экземпляры
                for auth in list_author:
                    new_article = eLibrary_Library()
                    if "lastname" in auth:
                        #print(str(auth["lastname"]))
                        new_article.author = str(auth["lastname"])
                    if "initials" in auth:
                            new_article.author = new_article.author + " " + str(auth["initials"])
                    count_author_temp += 1
                    all_elibrary_list_library.append(new_article)
            
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
            #год
            if "source" in e:
                if "issue" in e["source"]:
                    if "year" in e["source"]["issue"]:
                        all_elibrary_list_library[i].year = e["source"]["issue"]["year"]
            if all_elibrary_list_library[i].year == None:
                if "yearpubl" in e:
                    all_elibrary_list_library[i].year = e["yearpubl"]
            #ссылка
            if "linkurl" in e:
                all_elibrary_list_library[i].link = e["linkurl"]
            #doi
            if "doi" in e:
                all_elibrary_list_library[i].doi = e["doi"]
        count_all_author += count_author_temp

    for i in range(len(all_elibrary_list_library)):
        all_elibrary_list_library[i].author = Translite(all_elibrary_list_library[i].author)
        
    for i in range(len(all_elibrary_list_library)):
        all_elibrary_list_library[i].clear_title = "".join(e for e in all_elibrary_list_library[i].title.lower() if e.isalpha())
        
    for i in range(len(all_elibrary_list_library)):
        all_elibrary_list_library[i].clear_author = "".join(e for e in all_elibrary_list_library[i].author if e.isupper())

    print("Запись в файл началась eLibrary")
    with open("Source/eLibrary/Result.txt", "w", encoding="utf-8") as file:
        for index, val in enumerate(all_elibrary_list_library):
            file.write("Запись №: " + str(index) + "\n")
            file.write(val.Print())
            file.write("\n\n\n")
    print("Запись в файл закончилась eLibrary")
    return all_elibrary_list_library, "eLibrary"
