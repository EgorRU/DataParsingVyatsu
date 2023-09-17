from async_tkinter_loop import async_mainloop
from GUI.Window import win
from Parsing.Scopus import Scopus
from Parsing.Wos import Wos
from Parsing.iPublishing import IPublishing
from Parsing.eLibrary import eLibrary
from Parsing.Equals import Equals, IPublishingEquals


def main():
    #Equals(Scopus("Source/Scopus/Scopus1.xlsx"), Scopus("Source/Scopus/Scopus2.xlsx"))

    #Equals(Wos("Source/Wos/Wos1.xlsx"), Wos("Source/Wos/Wos2.xlsx"))

    #IPublishingEquals(Wos("Source/Wos/Wos1.xlsx"), IPublishing("Source/IPublishing/IPublishing.xlsx"))

    #IPublishingEquals(Scopus("Source/Scopus/Scopus1.xlsx"), IPublishing("Source/IPublishing/IPublishing.xlsx"))

    #eLibrary("Source/eLibrary/Ipunisher.xml")
    async_mainloop(win)
    print("Завершение программы")
    

if __name__ == "__main__":
     main()

