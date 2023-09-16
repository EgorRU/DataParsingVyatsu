import json
import xmltodict


def eLibrary():
    file = open("Source/eLibrary/Ipunisher.xml", 'br')
    s = ""
    symbol = s.encode("utf-8")
    data = file.read()
    data = data.replace(symbol, b"")
    file.close()
    

    file = open("Source/eLibrary/Ipunisher.xml", 'bw')
    file.write(data)
    file.close()


    file = open("Source/eLibrary/Ipunisher.xml", "r", encoding="utf-8")
    data = file.read()
    dict_data = xmltodict.parse(data)
    json_data = json.dumps(dict_data, ensure_ascii=False, indent=4)
    file.close()
    

    file = open("Source/eLibrary/Ipunisher.py", "w", encoding="utf-8")
    file.write("dictionary = ")
    file.write(json_data)
    file.close()


