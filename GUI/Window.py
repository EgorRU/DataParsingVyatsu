from async_tkinter_loop import async_handler
from tkinter import *
from tkinter.constants import NORMAL
from tkinter import ttk
from tkinter import messagebox
import tkinter, os
import tkinter.filedialog
from Parsing.Scopus import Scopus
from Parsing.Wos import Wos
from Parsing.iPublishing import IPublishing
from Parsing.eLibrary import eLibrary
from Parsing.Equals import Equals, IPublishingEquals

win = Tk()

#списки со статьями
list_scopus = []
list_wos = []
list_elibrary = []
list_ipublishing = []

lst = []

left_table_create = False
right_table_create = False


@async_handler
async def on_closing():
    if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
        win.destroy()


async def open_file_Scopus_left():
    ftypes = [('xls', 'xlsx')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))  # окошко открытия файла
    filename = dlg.show()  #получение имени файла для дальнейшей работы
    if len(filename) > 0:  #если не пустое имя файла

        # переменные чтоб понимать что было загружено в таблицу 'w' - WoS, 's' - Scopus, 'i' - iPublishing, 'e' - eLibrary
        global left_table_site
        global right_table_site
        left_table_site = 's'
        if 'right_table_site' not in locals():
            right_table_site = ''
        if ((left_table_site == 's' and right_table_site == 's') or
                (left_table_site == 'i' and right_table_site == 's') or
                (left_table_site == 's' and right_table_site == 'i')):
            mainmenu.entryconfigure(3, state=NORMAL)  # разблокирование кнопки сравнить данные

        #обработка файла, получение списка данных
        list_scopus_tuple = Scopus(filename)
        print("Scopus успешно загружен и обработан программой")
        list_scopus = list_scopus_tuple[0]
        scopus_source = list_scopus_tuple[1]
        lst = []
        for i in range(len(list_scopus)):
            lst.append((list_scopus[i].author, list_scopus[i].title, list_scopus[i].year,
                        list_scopus[i].link, list_scopus[i].citation))

        table_left_temp.destroy()
        global left_table_create
        global table_left
        if left_table_create == True:
            table_left.destroy()
        heads = ['author', 'title', 'year', 'link', 'citation']  # столбики
        table_left = ttk.Treeview(frametableleft, show='headings')  # инициализация таблицы
        table_left['columns'] = heads  # привязка столбцов к таблице
        left_table_create = True

        for header in heads:  # для каждого столбика выравниваем по центру все ячейки
            table_left.heading(header, text=header, anchor='center')
            table_left.column(header, anchor='center')

        scroll_pane = ttk.Scrollbar(frametableleft, command=async_handler(table_left.yview))
        table_left.configure(yscrollcommand=scroll_pane.set)
        scroll_pane.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        table_left.pack(expand=tkinter.YES,
                        fill=tkinter.BOTH)  # штука которая увеличивает таблицу в зависимости от кол-ва строк

        for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
            table_left.insert('', tkinter.END, values=row)  # без неё слева будет большой пропуск т к предуматривается полноценная иерархия

        table_left.column("author", minwidth=0, width=100, stretch=NO)
        table_left.column("title", minwidth=0, width=330, stretch=YES)
        table_left.column("year", minwidth=0, width=40, stretch=NO)
        table_left.column("link", minwidth=0, width=180, stretch=NO)
        table_left.column("citation", minwidth=0, width=60, stretch=NO)


async def open_file_Scopus_right():
    ftypes = [('xls', 'xlsx')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))  # окошко открытия файла
    filename = dlg.show()  #получение имени файла для дальнейшей работы
    if len(filename) > 0:  #если не пустое имя файла

        # переменные чтоб понимать что было загружено в таблицу 'w' - WoS, 's' - Scopus, 'i' - iPublishing, 'e' - eLibrary
        global left_table_site
        global right_table_site
        right_table_site = 's'
        if 'left_table_site' not in locals():
            left_table_site = ''
        if ((left_table_site == 's' and right_table_site == 's') or
                (left_table_site == 'i' and right_table_site == 's') or
                (left_table_site == 's' and right_table_site == 'i')):
            mainmenu.entryconfigure(3, state=NORMAL)  # разблокирование кнопки сравнить данные

        #обработка файла, получение списка данных
        list_scopus_tuple = Scopus(filename)
        print("Scopus успешно загружен и обработан программой")
        list_scopus = list_scopus_tuple[0]
        scopus_source = list_scopus_tuple[1]
        lst = []
        for i in range(len(list_scopus)):
            lst.append((list_scopus[i].author, list_scopus[i].title, list_scopus[i].year, list_scopus[i].link, list_scopus[i].citation))

        table_right_temp.destroy()
        global right_table_create
        if right_table_create == True:
            table_right.destroy()
        heads = ['author', 'title', 'year', 'link', 'citation']  # столбики
        table_right = ttk.Treeview(frametableright, show='headings')  # инициализация таблицы
        table_right['columns'] = heads  # привязка столбцов к таблице
        right_table_create = True

        for header in heads:  # для каждого столбика выравниваем по центру все ячейки
            table_right.heading(header, text=header, anchor='center')
            table_right.column(header, anchor='center')

        scroll_pane = ttk.Scrollbar(frametableright, command=table_right.yview)
        table_right.configure(yscrollcommand=scroll_pane.set)
        scroll_pane.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        table_right.pack(expand=tkinter.YES, fill=tkinter.BOTH)  # штука которая увеличивает таблицу в зависимости от кол-ва строк

        for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
            table_right.insert('', tkinter.END, values=row)  # без неё слева будет большой пропуск т к предуматривается полноценная иерархия

        table_right.column("author", minwidth=0, width=100, stretch=NO)
        table_right.column("title", minwidth=0, width=330, stretch=YES)
        table_right.column("year", minwidth=0, width=40, stretch=NO)
        table_right.column("link", minwidth=0, width=180, stretch=NO)
        table_right.column("citation", minwidth=0, width=60, stretch=NO)


async def open_file_WoS_left():
    ftypes = [('xls', 'xlsx')] #допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__)) #окошко открытия файла
    filename = dlg.show() #получение имени файла для дальнейшей работы
    if len(filename)> 0: #если не пустое имя файла

        # переменные чтоб понимать что было загружено в таблицу 'w' - WoS, 's' - Scopus, 'i' - iPublishing, 'e' - eLibrary
        global left_table_site
        global right_table_site
        left_table_site = 'w'
        if 'right_table_site' not in locals():
            right_table_site = ''
        if ((left_table_site == 'w' and right_table_site == 'w') or
                (left_table_site == 'i' and right_table_site == 'w') or
                (left_table_site == 'w' and right_table_site == 'i')):
            mainmenu.entryconfigure(3, state=NORMAL)  # разблокирование кнопки сравнить данные

        #обработка файла, получение списка данных
        list_wos_tuple = Wos(filename)
        print("Wos успешно загружен и обработан программой")
        list_wos = list_wos_tuple[0]
        wos_source = list_wos_tuple[1]

        lst = []
        for i in range(len(list_wos)):
            lst.append((list_wos[i].author, list_wos[i].title, list_wos[i].year, list_wos[i].link, list_wos[i].volume))

        table_left_temp.destroy()
        global left_table_create
        if left_table_create == True:
            table_left.destroy()
        heads = ['author', 'title', 'year', 'link', 'volume']  # столбики
        table_left = ttk.Treeview(frametableleft, show='headings')  # инициализация таблицы
        table_left['columns'] = heads  # привязка столбцов к таблице
        left_table_create = True

        for header in heads:  # для каждого столбика выравниваем по центру все ячейки
            table_left.heading(header, text=header, anchor='center')
            table_left.column(header, anchor='center')

        scroll_pane = ttk.Scrollbar(frametableleft, command=table_left.yview)
        table_left.configure(yscrollcommand=scroll_pane.set)
        scroll_pane.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        table_left.pack(expand=tkinter.YES, fill=tkinter.BOTH)  # штука которая увеличивает таблицу в зависимости от кол-ва строк

        for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
            table_left.insert('', tkinter.END, values=row)  # без неё слева будет большой пропуск т к предуматривается полноценная иерархия

        table_left.column("author", minwidth=0, width=100, stretch=NO)
        table_left.column("title", minwidth=0, width=330, stretch=YES)
        table_left.column("year", minwidth=0, width=40, stretch=NO)
        table_left.column("link", minwidth=0, width=180, stretch=NO)
        table_left.column("volume", minwidth=0, width=60, stretch=NO)


async def open_file_WoS_right():
    ftypes = [('xls', 'xlsx')] #допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__)) #окошко открытия файла
    filename = dlg.show() #получение имени файла для дальнейшей работы
    if len(filename)> 0: #если не пустое имя файла

        # переменные чтоб понимать что было загружено в таблицу 'w' - WoS, 's' - Scopus, 'i' - iPublishing, 'e' - eLibrary
        global left_table_site
        global right_table_site
        right_table_site = 'w'
        if 'left_table_site' not in locals():
            left_table_site = ''
        if ((left_table_site == 'w' and right_table_site == 'w') or
                (left_table_site == 'i' and right_table_site == 'w') or
                (left_table_site == 'w' and right_table_site == 'i')):
            mainmenu.entryconfigure(3, state=NORMAL)  # разблокирование кнопки сравнить данные

        #обработка файла, получение списка данных
        list_wos_tuple = Wos(filename)
        print("Wos успешно загружен и обработан программой")
        list_wos = list_wos_tuple[0]
        wos_source = list_wos_tuple[1]
        lst = []
        for i in range(len(list_wos)):
            lst.append((list_wos[i].author, list_wos[i].title, list_wos[i].year, list_wos[i].link, list_wos[i].volume))

        table_right_temp.destroy()
        global right_table_create
        if right_table_create == True:
            table_right.destroy()
        heads = ['author', 'title', 'year', 'link', 'volume']  # столбики
        table_right = ttk.Treeview(frametableright, show='headings')  # инициализация таблицы
        table_right['columns'] = heads  # привязка столбцов к таблице
        right_table_create = True

        for header in heads:  # для каждого столбика выравниваем по центру все ячейки
            table_right.heading(header, text=header, anchor='center')
            table_right.column(header, anchor='center')

        scroll_pane = ttk.Scrollbar(frametableright, command=table_right.yview)
        table_right.configure(yscrollcommand=scroll_pane.set)
        scroll_pane.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        table_right.pack(expand=tkinter.YES, fill=tkinter.BOTH)  # штука которая увеличивает таблицу в зависимости от кол-ва строк

        for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
            table_right.insert('', tkinter.END, values=row)  # без неё слева будет большой пропуск т к предуматривается полноценная иерархия

        table_right.column("author", minwidth=0, width=100, stretch=NO)
        table_right.column("title", minwidth=0, width=330, stretch=YES)
        table_right.column("year", minwidth=0, width=40, stretch=NO)
        table_right.column("link", minwidth=0, width=180, stretch=NO)
        table_right.column("volume", minwidth=0, width=60, stretch=NO)


async def open_file_Elibrary_left():
    ftypes = [('All files','*')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))  # окошко открытия файла
    filename = dlg.show()  # получение имени файла для дальнейшей работы
    if len(filename) > 0:  # если не пустое имя файла

        list_Elibrary_tuple = eLibrary(filename)
        print("Elibrary успешно загружен и обработан программой")
        list_Elibrary = list_Elibrary_tuple[0]
        Elibrary_source = list_Elibrary_tuple[1]

        left_table_site = 'e'
        if ((left_table_site == 'e' and right_table_site == 'e') or
                (left_table_site == 'i' and right_table_site == 'e') or
                (left_table_site == 'e' and right_table_site == 'i')):
            mainmenu.entryconfigure(3, state=NORMAL)  # разблокирование кнопки сравнить данные


async def open_file_Elibrary_right():
    ftypes = [('All files','*')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))  # окошко открытия файла
    filename = dlg.show()  # получение имени файла для дальнейшей работы
    if len(filename) > 0:  # если не пустое имя файла

        list_Elibrary_tuple = eLibrary(filename)
        print("Elibrary успешно загружен и обработан программой")
        list_Elibrary = list_Elibrary_tuple[0]
        Elibrary_source = list_Elibrary_tuple[1]

        right_table_site = 'e'
        if ((left_table_site == 'e' and right_table_site == 'e') or
                (left_table_site == 'i' and right_table_site == 'e') or
                (left_table_site == 'e' and right_table_site == 'i')):
            mainmenu.entryconfigure(3, state=NORMAL)  # разблокирование кнопки сравнить данные


async def open_file_Ipublishing_left():
    ftypes = [('xls', 'xlsx')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))  # окошко открытия файла
    filename = dlg.show()  # получение имени файла для дальнейшей работы
    if len(filename) > 0:  # если не пустое имя файла
        # переменные чтоб понимать что было загружено в таблицу 'w' - WoS, 's' - Scopus, 'i' - iPublishing, 'e' - eLibrary
        global left_table_site
        global right_table_site
        left_table_site = 'i'
        mainmenu.entryconfigure(3, state=NORMAL)  # разблокирование кнопки сравнить данные
        list_ipublishing_tuple = IPublishing(filename)
        print("IPublishing успешно загружен и обработан программой")
        list_ipublishing = list_ipublishing_tuple[0]
        ipublishing_source = list_ipublishing_tuple[1]
        lst = []
        for i in range(len(list_ipublishing)):
            lst.append((list_ipublishing[i].author, list_ipublishing[i].title, list_ipublishing[i].year, list_ipublishing[i].article, list_ipublishing[i].link))

        table_left_temp.destroy()
        global left_table_create
        if left_table_create == True:
            table_left.destroy()
        heads = ['author', 'title', 'year', 'article', 'link']  # столбики
        table_left = ttk.Treeview(frametableleft, show='headings')  # инициализация таблицы
        table_left['columns'] = heads  # привязка столбцов к таблице
        left_table_create = True

        for header in heads:  # для каждого столбика выравниваем по центру все ячейки
            table_left.heading(header, text=header, anchor='center')
            table_left.column(header, anchor='center')

        scroll_pane = ttk.Scrollbar(frametableleft, command=table_left.yview)
        table_left.configure(yscrollcommand=scroll_pane.set)
        scroll_pane.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        table_left.pack(expand=tkinter.YES, fill=tkinter.BOTH)  # штука которая увеличивает таблицу в зависимости от кол-ва строк

        for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
            table_left.insert('', tkinter.END, values=row)  # без неё слева будет большой пропуск т к предуматривается полноценная иерархия

        table_left.column("author", minwidth=0, width=100, stretch=NO)
        table_left.column("title", minwidth=0, width=250, stretch=YES)
        table_left.column("year", minwidth=0, width=40, stretch=NO)
        table_left.column("article", minwidth=0, width=160, stretch=NO)
        table_left.column("link", minwidth=0, width=160, stretch=NO)


async def open_file_Ipublishing_right():
    ftypes = [('xls', 'xlsx')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))  # окошко открытия файла
    filename = dlg.show()  # получение имени файла для дальнейшей работы
    if len(filename) > 0:  # если не пустое имя файла
        # переменные чтоб понимать что было загружено в таблицу 'w' - WoS, 's' - Scopus, 'i' - iPublishing, 'e' - eLibrary
        global left_table_site
        global right_table_site
        right_table_site = 's'
        mainmenu.entryconfigure(3, state=NORMAL)  # разблокирование кнопки сравнить данные
        list_ipublishing_tuple = IPublishing(filename)
        print("IPublishing успешно загружен и обработан программой")
        list_ipublishing = list_ipublishing_tuple[0]
        ipublishing_source = list_ipublishing_tuple[1]
        lst = []
        for i in range(len(list_ipublishing)):
            lst.append((list_ipublishing[i].author, list_ipublishing[i].title, list_ipublishing[i].year, list_ipublishing[i].article, list_ipublishing[i].link))

        table_right_temp.destroy()
        global right_table_create
        if right_table_create == True:
            table_right.destroy()
        heads = ['author', 'title', 'year', 'article', 'link']  # столбики
        table_right = ttk.Treeview(frametableright, show='headings')  # инициализация таблицы
        table_right['columns'] = heads  # привязка столбцов к таблице
        right_table_create = True

        for header in heads:  # для каждого столбика выравниваем по центру все ячейки
            table_right.heading(header, text=header, anchor='center')
            table_right.column(header, anchor='center')

        scroll_pane = ttk.Scrollbar(frametableright, command=table_right.yview)
        table_right.configure(yscrollcommand=scroll_pane.set)
        scroll_pane.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        table_right.pack(expand=tkinter.YES, fill=tkinter.BOTH)  # штука которая увеличивает таблицу в зависимости от кол-ва строк

        for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
            table_right.insert('', tkinter.END, values=row)  # без неё слева будет большой пропуск т к предуматривается полноценная иерархия

        table_right.column("author", minwidth=0, width=100, stretch=NO)
        table_right.column("title", minwidth=0, width=250, stretch=YES)
        table_right.column("year", minwidth=0, width=40, stretch=NO)
        table_right.column("article", minwidth=0, width=160, stretch=NO)
        table_right.column("link", minwidth=0, width=160, stretch=NO)

        list_Ipublishing = []
        
#кнопка Сравнение
async def open_compare_window():
    comparewin = Toplevel(win) #инициализация
    comparewin.geometry('750x700')  #размер
    comparewin.title("Результат сравнения") #название
    frame_compare_button = Frame(comparewin) #задаем поле
    frame_compare_table = Frame(comparewin)  #задаем поле
    frame_compare_button.place(relx=0, rely=0, relwidth=1, relheight=0.05)  #размещаем его на весь размер окна
    frame_compare_table.place(relx=0, rely=0.05, relwidth = 1, relheight = 0.95) #размещаем его на весь размер окна
    unload_to_xlsx = Button(frame_compare_button)
    unload_to_xlsx.place(relx=0.475, rely = 0, relwidth = 0.05, relheight = 0.05)

    # Затычки для таблиц
    heads = [' ', ' ', ' ', ' ', ' ']  # столбики
    table_temp = ttk.Treeview(frame_compare_table, show='headings')  # инициализация таблицы
    table_temp['columns'] = heads  # привязка столбцов к таблице

    for header in heads:  # для каждого столбика выравниваем по центру все ячейки
        table_temp.heading(header, text=header, anchor='center')
        table_temp.column(header, anchor='center')

    scroll_pane = ttk.Scrollbar(frame_compare_table, command=async_handler(table_temp.yview))
    table_temp.configure(yscrollcommand=scroll_pane.set)
    scroll_pane.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    table_temp.pack(expand=tkinter.YES, fill=tkinter.BOTH)  # штука которая увеличивает таблицу в зависимости от кол-ва строк


#кнопка HELP
async def open_help_window():
    helpwin = Toplevel(win) #инициализация
    helpwin.geometry('600x225')  #размер
    helpwin.title("Окно помощи") #название
    helpwin.resizable(False, False) #запрещаем менять размер
    framehelp = Frame(helpwin) #задаем поле
    framehelp.place(relx=0, rely = 0, relwidth = 1, relheight = 1) #размещаем его на весь размер окна
    l1 = Label(framehelp, text = "Загрузите файлы в каждую из таблиц через Файл->Загрузить->\n\n" +
                                 "Если загруженнные файлы с одинакового сайта или один из файлов iPublishing\n" +
                                 "то станет доступна кнопка Сравнить данные \n\n" +
                                 "Кнопка Выгрузить в XML/XLS выгружает результаты сравнения\n "
                                 "в выбраный формат\n")
    l1.pack() #создаем текст и размещаем по центру


#создание окна
win['bg'] = '#fafafa' #цвет
win.title('Library') #название
win.geometry('1500x700') #размер
win.protocol("WM_DELETE_WINDOW", on_closing) #событие при закрытии приложения
win.minsize(1500, 700)

#блоки основного окна
frametableleft = Frame(win, bg = '#ffb370')
frametableright = Frame(win, bg = '#ffb370')

#расположение блоков, чтоб можно было менять размер окна
frametableleft.place(relx=0, rely = 0, relwidth = 0.5, relheight = 1)
frametableright.place(relx=0.5, rely = 0, relwidth = 0.5, relheight = 1)

#меню
mainmenu = Menu(win)
win.config(menu=mainmenu)

#создание самого меню
filemenu = Menu(mainmenu, tearoff=0)

#создание поля загрузка файлов
filemenu_load = Menu(filemenu, tearoff=0)

filemenu_load_WoF = Menu(filemenu_load, tearoff=0)
filemenu_load_WoF.add_command(label="Загрузить в левую таблицу",command = async_handler(open_file_WoS_left))
filemenu_load_WoF.add_command(label="Загрузить в правую таблицу",command = async_handler(open_file_WoS_right))
filemenu_load.add_cascade(label="Загрузить Web of Science", menu = filemenu_load_WoF)

filemenu_load_Scopus = Menu(filemenu_load, tearoff=0)
filemenu_load_Scopus.add_command(label="Загрузить в левую таблицу",command = async_handler(open_file_Scopus_left))
filemenu_load_Scopus.add_command(label="Загрузить в правую таблицу",command = async_handler(open_file_Scopus_right))
filemenu_load.add_cascade(label="Загрузить Scopus", menu = filemenu_load_Scopus)

filemenu_load_Elibrary = Menu(filemenu_load, tearoff=0)
filemenu_load_Elibrary.add_command(label="Загрузить в левую таблицу",command = async_handler(open_file_Elibrary_left))
filemenu_load_Elibrary.add_command(label="Загрузить в правую таблицу",command = async_handler(open_file_Elibrary_right))
filemenu_load.add_cascade(label="Загрузить Elibrary", menu = filemenu_load_Elibrary)

filemenu_load_Ipublishing = Menu(filemenu_load, tearoff=0)
filemenu_load_Ipublishing.add_command(label="Загрузить в левую таблицу",command = async_handler(open_file_Ipublishing_left))
filemenu_load_Ipublishing.add_command(label="Загрузить в правую таблицу",command = async_handler(open_file_Ipublishing_right))
filemenu_load.add_cascade(label="Загрузить Ipublishing", menu = filemenu_load_Ipublishing)

filemenu.add_cascade(label="Загрузить файл", menu = filemenu_load)


#создание поля выгрузка файлов
filemenu_unload = Menu(filemenu, tearoff=0)
filemenu_unload.add_command(label="Выгрузить файл в xlsx")
filemenu_unload.add_command(label="Выгрузить файл в xml")
filemenu.add_cascade(label="Выгрузить файл", menu = filemenu_unload)

#создание главных полей
mainmenu.add_cascade(label="Файл", menu=filemenu)
mainmenu.add_cascade(label="Справка", command = async_handler(open_help_window))
mainmenu.add_cascade(label="Сравнить данные", command = async_handler(open_compare_window), state = DISABLED) #пока окошка хелпа выведет

#Затычки для таблиц
heads = [' ', ' ', ' ', ' ', ' ']  # столбики
table_left_temp = ttk.Treeview(frametableleft, show='headings')  # инициализация таблицы
table_left_temp['columns'] = heads  # привязка столбцов к таблице

for header in heads:  # для каждого столбика выравниваем по центру все ячейки
    table_left_temp.heading(header, text=header, anchor='center')
    table_left_temp.column(header, anchor='center')

scroll_pane = ttk.Scrollbar(frametableleft, command=table_left_temp.yview)
table_left_temp.configure(yscrollcommand=scroll_pane.set)
scroll_pane.pack(side=tkinter.RIGHT, fill=tkinter.Y)
table_left_temp.pack(expand=tkinter.YES, fill=tkinter.BOTH)  # штука которая увеличивает таблицу в зависимости от кол-ва строк


heads = [' ', ' ', ' ', ' ', ' ']  # столбики
table_right_temp = ttk.Treeview(frametableright, show='headings')  # инициализация таблицы
table_right_temp['columns'] = heads  # привязка столбцов к таблице

for header in heads:  # для каждого столбика выравниваем по центру все ячейки
    table_right_temp.heading(header, text=header, anchor='center')
    table_right_temp.column(header, anchor='center')

scroll_pane = ttk.Scrollbar(frametableright, command=table_right_temp.yview)
table_right_temp.configure(yscrollcommand=scroll_pane.set)
scroll_pane.pack(side=tkinter.RIGHT, fill=tkinter.Y)
table_right_temp.pack(expand=tkinter.YES, fill=tkinter.BOTH)  # штука которая увеличивает таблицу в зависимости от кол-ва строк
