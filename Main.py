from async_tkinter_loop import async_mainloop
from GUI.Window import win
from Parsing.Scopus import Scopus
from Parsing.Wos import Wos
from Parsing.iPublishing import IPublishing
from Parsing.eLibrary import eLibrary
from Parsing.Equals import identical_sources_equals, different_source_equals
from Upload import Upload


def main():
    #scopus
    #list1, list2, list3 = identical_sources_equals(Scopus("Source/Scopus/Scopus1.xlsx")[0], Scopus("Source/Scopus/Scopus2.xlsx")[0])
    #Upload(list1, list2, list3)

    #wos
    #list1, list2, list3 = identical_sources_equals(Wos("Source/Wos/Wos1.xlsx")[0], Wos("Source/Wos/Wos2.xlsx")[0])
    #Upload(list1, list2, list3)
    
    #ipublishing scopus
    #list1, list2, list3 = different_source_equals(Scopus("Source/Scopus/Scopus1.xlsx")[0], IPublishing("Source/IPublishing/IPublishing.xlsx")[0])
    #Upload(list1, list2, list3)

    #ipublishing wos
    #list1, list2, list3 = different_source_equals(Wos("Source/Wos/Wos1.xlsx")[0], IPublishing("Source/IPublishing/IPublishing.xlsx")[0])
    #Upload(list1, list2, list3)

    #ipublishing eLibrary
    #list1, list2, list3 = different_source_equals(eLibrary("Source/eLibrary/Ipunisher.xml")[0], IPublishing("Source/IPublishing/IPublishing.xlsx")[0])
    #Upload(list1, list2, list3)

    async_mainloop(win)
    print("Завершение программы")
    

if __name__ == "__main__":
     main()

