def clear_author(string):  
    #убираем лишние символы из строки и делаем нижний регистр
    new_str = ""
    if string != None and len(string)>0:
        string = string.lower()
        string = string[0].upper() + string[1:]
        for i in range (len(string)):
            if string[i].isalpha() or string[i]==" " or string[i]==".":
                new_str += string[i]
           
        #приводим строку к единому виду
        new = new_str.split()
        #если было три элемента то, делаем инициалы и фамилию
        if len(new)==3:
            #если строка не сломана
            if new[2]!=".":
                new[0] = new[0][0].upper() + new[0][1:]
                new[1] = f"{new[1][0].upper()}"
                if new[2][0]==".":
                    new[2] = f"{new[2][1].upper()}"
                else:
                    new[2] = f"{new[2][0].upper()}"
                new_str = f"{new[0]} {new[1]}.{new[2]}."
            #если строка сломана
            else:
                #фамилия
                new[0] = new[0][0].upper() + new[0][1:]
                ii = 0
                while new[1][ii]==".":
                    ii += 1
                #первые инициалы
                new_str_1 = f"{new[1][ii].upper()}"
                #вторые инициалы
                while len(new[1])-1>=ii and new[1][ii]!=".":
                    ii += 1
                ii += 1
                if len(new[1])-1 >=  ii:
                    new_str_2 = f"{new[1][ii].upper()}"
                    new_str = f"{new[0]} {new_str_1}.{new_str_2}."
                else:
                    new_str = f"{new[0]} {new_str_1}." 
        #если было два элемента, то возможны случаи, когда есть фул имя или инициалы склеены между собой
        if len(new)==2:
            #если склеены инициалы
            counter = new[1].count('.')
            #если есть две точки
            if counter==2:
                #фамилия
                new[0] = new[0][0].upper() + new[0][1:]
                #инициалы
                ii = 0
                while new[1][ii]==".":
                    ii += 1
                new_str_1 = f"{new[1][ii].upper()}"
                while len(new[1])-1>=ii and new[1][ii]!=".":
                    ii += 1
                ii += 1
                if len(new[1])-1 >=  ii:
                    new_str_2 = f"{new[1][ii].upper()}"
                    new_str = f"{new[0]} {new_str_1}.{new_str_2}."
                else:
                    new_str = f"{new[0]} {new_str_1}."
            #если точек нет, то смотрим сколько букв
            elif counter==0:
                if len(new[1])==1:
                    new[0] = new[0][0].upper() + new[0][1:]
                    new_str = f"{new[1][0].upper()}"
                    new_str = f"{new[0]} {new_str}."
                else:
                    new[0] = new[0][0].upper() + new[0][1:]
                    new_str_1 = f"{new[1][0].upper()}"
                    new_str_2 = f"{new[1][1].upper()}"
                    new_str = f"{new[0]} {new_str_1}.{new_str_2}."
            #если одна точки - одна буква с инициалами
            else:
                new[0] = new[0][0].upper() + new[0][1:]
                new_str = f"{new[0]} {new[1][0].upper()}."
                
    return new_str.replace("é","e").replace("É","E")


def clear_IPublishing_title(string):
    index = string.find("/")
    if len(string)>index and string[index+1]!='/':
        index += 1
        while len(string)>index and string[index]!='/':
            index += 1
    if index == -1 or len(string)<=index:
        return string
    #обрезаем всё до //
    new_str = string[:index].strip()
    #инвертируем
    new_str = new_str[::-1].strip()
    #находим первую точку
    index = 30
    while  (new_str[index]=='.' and new_str[index+1].isupper() and new_str[index+2]==' ' and new_str[index+3]=='.' and new_str[index+4].isupper() and (new_str[index+5]!="." and new_str[index+6]!="."))==False and \
           (new_str[index]==' ' and new_str[index+1].isupper() and new_str[index+2]==' ' and new_str[index+3]=='.' and new_str[index+4].isupper() and (new_str[index+5]!="." and new_str[index+6]!="."))==False and \
           (new_str[index]=='.' and new_str[index+1].isupper() and new_str[index+2]=='.' and new_str[index+3].isupper() and (new_str[index+4]!="." and new_str[index+5]!="."))==False and \
           (new_str[index]==' ' and new_str[index+1].isupper() and new_str[index+2]=='.' and new_str[index+3].isupper() and (new_str[index+4]!="." and new_str[index+5]!="."))==False and \
           (new_str[index]=='.' and new_str[index+1].isupper() and new_str[index+2]==' ' and new_str[index+3]==' ' and new_str[index+4]=='.' and new_str[index+5].isupper() and (new_str[index+6]!="." and new_str[index+7]!="."))==False:
        index += 1
        if index>=len(new_str):
            break
    new_str = new_str[:index]
    new_str = new_str[::-1].strip()
    if new_str[0]=="," or new_str[0]==".":
        new_str = new_str[1:].strip()
    if new_str[0]=="," or new_str[0]==".":
        new_str = new_str[1:].strip()
    return new_str