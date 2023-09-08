import tkinter, os
from tkinter import *
from tkinter.constants import DISABLED, NORMAL
from tkinter import ttk
from tkinter import messagebox
import tkinter.filedialog
from Parsing.Scopus import Scopus
from Parsing.Wos import Wos
from Parsing.iPublishing import IPublishing
from Сomparison.Scopus_eq import Eg_scopus

win = Tk()

#списки со статьями
list_scopus = []
list_wos = []
list_elibrary = []
list_ipublishing = []
lst = []

#при закрытии
def on_closing():
    if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
        win.destroy()


def open_file_Scopus():
    ftypes = [('xls', 'xlsx')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))  # окошко открытия файла
    filename = dlg.show()  #получение имени файла для дальнейшей работы
    if len(filename) > 0:  #если не пустое имя файла
        mainmenu.entryconfigure(3, state=NORMAL)  # разблокирование кнопки сравнить данные
        #обработка файла, получение списка данных
        list_scopus=Scopus(filename)
        print("Scopus успешно загружен и обработан программой")

        heads = ['author', 'title', 'year', 'link', 'citation']
        table_left = ttk.Treeview(frametableleft, show='headings')  # инициализация таблицы
        table_left['columns'] = heads  # привязка столбцов к таблице
        for i in range(len(list_scopus)):
            lst.append((list_scopus[i].author, list_scopus[i].title, list_scopus[i].year,
                        list_scopus[i].link, list_scopus[i].citation))

        for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
            table_left.insert('', tkinter.END,
                         values=row)  # без неё слева будет большой пропуск т к предуматривается полноценная иерархия


def open_file_WoS():
    ftypes = [('xls', 'xlsx')] #допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__)) #окошко открытия файла
    filename = dlg.show() #получение имени файла для дальнейшей работы
    if len(filename)> 0: #если не пустое имя файла
        mainmenu.entryconfigure(3, state=NORMAL) #разблокирование кнопки сравнить данные
        #обработка файла, получение списка данных
        list_wos=Wos(filename)
        print("Wos успешно загружен и обработан программой")

        heads = ['author', 'title', 'year', 'link', 'volume']
        table_left = ttk.Treeview(frametableleft, show='headings')  # инициализация таблицы
        table_left['columns'] = heads  # привязка столбцов к таблице

        for i in range(len(list_wos)):
            lst.append((list_wos[i].author, list_wos[i].title, list_wos[i].year,
                        list_wos[i].link, list_wos[i].volume))

        for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
            table_left.insert('', tkinter.END,
                         values=row)  # без неё слева будет большой пропуск т к предуматривается полноценная иерархия

        

def open_file_Elibrary():
    ftypes = [('xls', 'xlsx')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))  # окошко открытия файла
    filename = dlg.show()  # получение имени файла для дальнейшей работы
    if len(filename) > 0:  # если не пустое имя файла
        mainmenu.entryconfigure(3, state=NORMAL)  # разблокирование кнопки сравнить данные


def open_file_Ipublishing():
    ftypes = [('All files','*')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))  # окошко открытия файла
    filename = dlg.show()  # получение имени файла для дальнейшей работы
    if len(filename) > 0:  # если не пустое имя файла
        mainmenu.entryconfigure(3, state=NORMAL)  # разблокирование кнопки сравнить данные
        print("Пошла загрузка")
        list_ipublishing=IPublishing(filename)
        print("IPublishing успешно загружен и обработан программой")
        

#кнопка HELP
def open_help_window():
    helpwin = Toplevel(win) #инициализация
    helpwin.geometry('385x225')  #размер
    helpwin['bg'] = '#fafafa' #цвет
    helpwin.title("Окно помощи") #название
    helpwin.resizable(False, False) #запрещаем менять размер
    framehelp = Frame(helpwin, bg='#fafafa') #задаем поле
    framehelp.place(relx=0, rely = 0, relwidth = 1, relheight = 1) #размещаем его на весь размер окна
    l1 = Label(framehelp, text = "Нажмите на иконку нужного сайта и загрузите файл\n\n Кнопка обновить данные сверяет данные из файла \nс данными в базе данных и обновляет данные в базе\n\n Все изменения при обновлении в базу данных \nотмечены в таблице в левой части приложения\n\n Кнопка Выгрузить в XML/XLS выгружает данные\n из базы данных в XML/XLS формат\n")
    l1.pack() #создаем текст и размещаем по центру


#создание окна
win['bg'] = '#fafafa' #цвет
win.title('Library') #название
win.geometry('1500x700') #размер
win.protocol("WM_DELETE_WINDOW", on_closing) #событие при закрытии приложения
win.resizable(False, False)

#блоки основного окна
frametableleft = Frame(win, bg = '#ffb370') #блок с таблицей изменений
frametableright = Frame(win, bg = '#ffb370') #блок с таблицей изменений

#расположение блоков, чтоб можно было менять размер окна
frametableleft.place(relx=0, rely = 0, relwidth = 0.5, relheight = 1)
frametableright.place(relx=0.5, rely = 0, relwidth = 0.5, relheight = 1)

#кнопки
def left_circle():
    btn_upload_right_WoS = tkinter.Button(frametableleft, text='WoS', command=open_file_WoS)
    btn_upload_right_WoS.place()


btn_upload_right = tkinter.Button(frametableright,text = 'Загрузить файл', command = left_circle)
btn_upload_right.place(relx=0.42, rely = 0.07, relwidth = 0.16, relheight = 0.07)

#меню
mainmenu = Menu(win)
win.config(menu=mainmenu)

filemenu = Menu(mainmenu, tearoff=0) #создание самого меню

filemenu_load = Menu(filemenu, tearoff=0) #создание поля загрузка файлов
filemenu_load.add_command(label="Загрузить Web of Science",command = open_file_WoS)
filemenu_load.add_command(label="Загрузить Scopus", command = open_file_Scopus)
filemenu_load.add_command(label="Загрузить Elibrary", command = open_file_Elibrary)
filemenu_load.add_command(label="Загрузить Ipublishing", command = open_file_Ipublishing)
filemenu.add_cascade(label="Загрузить файл", menu = filemenu_load)


filemenu_unload = Menu(filemenu, tearoff=0) #создание поля выгрузка файлов
filemenu_unload.add_command(label="Выгрузить файл в xlsx")
filemenu_unload.add_command(label="Выгрузить файл в xml")
filemenu.add_cascade(label="Выгрузить файл", menu = filemenu_unload)

mainmenu.add_cascade(label="Файл", menu=filemenu) #создание поля загрузка файлов
mainmenu.add_cascade(label="Справка", command = open_help_window) #создание поля справки


heads = ['', '', '', '', ''] #столбики
table_left = ttk.Treeview(frametableleft, show = 'headings') #инициализация таблицы
table_left['columns'] = heads #привязка столбцов к таблице


for header in heads:  # для каждого столбика выравниваем по центру все ячейки
    table_left.heading(header, text=header, anchor='center')
    table_left.column(header, anchor='center')


scroll_pane = ttk.Scrollbar(frametableleft, command=table_left.yview)
table_left.configure(yscrollcommand=scroll_pane.set)
scroll_pane.pack(side = tkinter.RIGHT,fill= tkinter.Y)
table_left.pack(expand = tkinter.YES, fill = tkinter.BOTH) #штука которая увеличивает таблицу в зависимости от кол-ва строк
