from async_tkinter_loop import async_mainloop
from GUI.Window import win
from Parsing.Scopus import Scopus
from Parsing.Wos import Wos
from Parsing.iPublishing import IPublishing
from Parsing.eLibrary import eLibrary
from Parsing.Equals import identical_sources_equals, different_source_equals
from Upload import Upload


def main():
    
    async_mainloop(win)
    print("Завершение программы")
    

if __name__ == "__main__":
     main()

