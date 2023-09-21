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
    #_, _, _, list1, list2, list3 = identical_sources_equals(Scopus("Source/Scopus/Scopus1.xlsx")[0], Scopus("Source/Scopus/Scopus2.xlsx")[0])
    #Upload("", list_new=list1, flag=False)
    #Upload("", list_new=list1, list_ident=list2, list_remove=list3, flag=True)

    #wos
    #_, _, _, list1, list2, list3 = identical_sources_equals(Wos("Source/Wos/Wos1.xlsx")[0], Wos("Source/Wos/Wos2.xlsx")[0])
    #Upload("", list_new=list1, list_ident=list2, list_remove=list3, flag=True)
    
    #ipublishing scopus
    #_, _, _, list1, list2, list3 = different_source_equals(IPublishing("Source/IPublishing/IPublishing.xlsx")[0], Scopus("Source/Scopus/Scopus2.xlsx")[0])
    #Upload("", list_new=list1, list_ident=list2, list_remove=list3, flag=True)

    #ipublishing wos
    #_, _, _, list1, list2, list3 = different_source_equals(IPublishing("Source/IPublishing/IPublishing.xlsx")[0], Wos("Source/Wos/Wos2.xlsx")[0])
    #Upload("", list_new=list1, list_ident=list2, list_remove=list3, flag=True)

    #ipublishing eLibrary
    #_, _, _, list1, list2, list3 = different_source_equals(IPublishing("Source/IPublishing/IPublishing.xlsx")[0], eLibrary("Source/eLibrary/IPunisher.xml")[0])
    #Upload("", list_new=list1, list_ident=list2, list_remove=list3, flag=True)
    win.mainloop()
    

if __name__ == "__main__":
     main()

