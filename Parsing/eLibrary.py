import json
import xmltodict
from Class import eLibrary


def eLibrary(path):
    # ������ ������ eLibrary
    all_elibrary_list_library = []

    #�������� �� ��, ��� �������
    if path[-3:]!="xml":
        return all_elibrary_list_library, ""

    #������ �������� xml � ������� ���������� ������
    file = open(path, 'br')
    s = ""
    symbol = s.encode("utf-8")
    data = file.read()
    data = data.replace(symbol, b"")
    file.close()
    
    #�������������� ����
    file = open(path, 'bw')
    file.write(data)
    file.close()

    #������ ������ � ������ json �������
    file = open(path, "r", encoding="utf-8")
    data = file.read()
    dict_data = xmltodict.parse(data)
    file.close()
    
    with open("Source/eLibrary/eLibrary.json", 'w', encoding="utf-8") as file:
        json.dump(dict_data, file, ensure_ascii=False, indent=2)
     
    #������ json �������
    count_author = 0
    list_library = dict_data["items"]["item"]
    for e in list_library:
        list_author = e["authors"]["author"]
        for author in list_author:
            new_article = eLibrary()

    return all_elibrary_list_library, "eLibrary"
