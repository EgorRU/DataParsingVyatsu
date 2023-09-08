from Parsing.Scopus import Scopus

def Eg_scopus():
    scopus_1=Scopus("Source/Scopus/Scopus1.xlsx")
    scopus_2=Scopus("Source/Scopus/Scopus2.xlsx")
    new_list = []
    for i in range (len(scopus_2)):
        copy = False
        for j in range (len(scopus_1)):
            if scopus_2[i]==scopus_1[j]:
                copy = True
                break
        if copy==False:
             new_list.append(scopus_2[i])
             
    for i in range (len(new_list)):
        print(new_list[i].Print())
    print(str(len(scopus_2)-len(scopus_1))+" = "+str(len(new_list)))
    return new_list