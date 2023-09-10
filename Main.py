from GUI.Window import win
from Parsing.Scopus import Scopus
from Parsing.Wos import Wos
from Parsing.iPublishing import IPublishing
from Parsing.eLibrary import eLibrary
from Parsing.Equals import Equals, IPublishingEquals


def Main():
    #Equals(Scopus("Source/Scopus/Scopus1.xlsx"), Scopus("Source/Scopus/Scopus2.xlsx"))
    #print()
    #Equals(Wos("Source/Wos/Wos.xlsx"), Wos("Source/Wos/Wos2.xlsx"))
    #print()
    #Equals(Wos("Source/Wos/Wos.xlsx"), Scopus("Source/Scopus/Scopus1.xlsx"))
    #print()
    #IPublishingEquals(Scopus("Source/Scopus/Scopus1.xlsx"), IPublishing("Source/IPublishing/IPublishing.xlsx"))
    #IPublishingEquals(Wos("Source/Wos/Wos.xlsx"), IPublishing("Source/IPublishing/IPublishing.xlsx"))

    win.mainloop()
    print("Завершение программы")
    

if __name__ == "__main__":
    Main()
