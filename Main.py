from async_tkinter_loop import async_mainloop
from GUI.Window import win
from Parsing.Scopus import Scopus
from Parsing.Wos import Wos
from Parsing.iPublishing import IPublishing
from Parsing.eLibrary import eLibrary
from Parsing.Equals import identical_sources_equals, different_source_equalss


def main():
    #scopus
    #identical_sources_equals(Scopus("Source/Scopus/Scopus1.xlsx"), Scopus("Source/Scopus/Scopus2.xlsx"))

    #wos
    #identical_sources_equals(Wos("Source/Wos/Wos1.xlsx"), Wos("Source/Wos/Wos2.xlsx"))

    #ipublishing scopus
    #different_source_equalss(Wos("Source/Wos/Wos1.xlsx"), IPublishing("Source/IPublishing/IPublishing.xlsx"))

    #ipublishing wos
    #different_source_equalss(Scopus("Source/Scopus/Scopus1.xlsx"), IPublishing("Source/IPublishing/IPublishing.xlsx"))

    #ipublishing eLibrary
    #different_source_equalss(Wos("Source/Wos/Wos1.xlsx"), IPublishing("Source/IPublishing/IPublishing.xlsx"))

    async_mainloop(win)
    print("Завершение программы")
    

if __name__ == "__main__":
     main()

