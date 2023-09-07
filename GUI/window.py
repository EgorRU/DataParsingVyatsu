import tkinter, os
from tkinter import *
from tkinter.constants import DISABLED, NORMAL
from tkinter import ttk
from tkinter import messagebox
import tkinter.filedialog
from Replace.Scopus import Scopus
from Replace.Wos import Wos

win = Tk()

#при закрытии
def on_closing():
    if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
        win.destroy()


def open_file_Scopus():
    ftypes = [('xls', 'xlsx')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл',
                                  initialdir=os.path.abspath(__file__))  # окошко открытия файла
    filename = dlg.show()  # получение имени файла для дальнейшей работы
    if len(filename) > 0:  # если не пустое имя файла
        mainmenu.entryconfigure(3, state=NORMAL)  # разблокирование кнопки сравнить данные
        #обработка файла, получение списка данных
        list_scopus=Scopus(filename)
        print("Scopus успешно загружен и обработан программой")


def open_file_WoS():
    ftypes = [('xls', 'xlsx')] #допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__)) #окошко открытия файла
    filename = dlg.show() #получение имени файла для дальнейшей работы
    if len(filename)> 0: #если не пустое имя файла
        mainmenu.entryconfigure(3, state=NORMAL) #разблокирование кнопки сравнить данные
        #обработка файла, получение списка данных
        #list_wos=Wos(filename)
        print("Wos успешно загружен и обработан программой")
        

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


#кнопка HELP
def open_help_window():
    helpwin = Toplevel(win) #инициализация
    helpwin.geometry('385x225')  #размер
    helpwin['bg'] = '#fafafa' #цвет
    helpwin.title("Окно помощи") #название
    helpwin.wm_attributes("-topmost",1) #помещаем поверх других окон
    helpwin.resizable(False, False) #запрещаем менять размер
    framehelp = Frame(helpwin, bg='#fafafa') #задаем поле
    framehelp.place(relx=0, rely = 0, relwidth = 1, relheight = 1) #размещаем его на весь размер окна
    l1 = Label(framehelp, text = "Нажмите на иконку нужного сайта и загрузите файл\n\n Кнопка обновить данные сверяет данные из файла \nс данными в базе данных и обновляет данные в базе\n\n Все изменения при обновлении в базу данных \nотмечены в таблице в левой части приложения\n\n Кнопка Выгрузить в XML/XLS выгружает данные\n из базы данных в XML/XLS формат\n")
    l1.pack() #созаем текст и размещаем по центру


#создание окна
win['bg'] = '#fafafa' #цвет
win.title('Library') #название
win.geometry('1500x700') #размер
win.wm_attributes("-topmost", 1) #окно будет поверх всех окон
win.protocol("WM_DELETE_WINDOW", on_closing) #событие при закрытии приложения
win.resizable(False, False)

#блоки основного окна
frametable = Frame(win, bg = '#ffb370') #блок с таблицей изменений

#расположение блоков, чтоб можно было менять размер окна
frametable.place(relx=0, rely = 0, relwidth = 1, relheight = 1)

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

helpmenu = Menu(mainmenu, tearoff=0) #создание поля помощь
helpmenu.add_command(label="Помощь",command=open_help_window)

mainmenu.add_cascade(label="Файл", menu=filemenu) #создание поля загрузка файлов
mainmenu.add_cascade(label="Справка", menu=helpmenu) #создание поля справки

mainmenu.add_cascade(label="Сравнить данные", menu=helpmenu, state=DISABLED) #создание кнопки сравнить

#большой лист для тестов
lst = [(1,'author', 'name', 2000),(1,'author', 'name', 2000), (1,'author', 'name', 2000),(1,'author', 'name', 2000),(1,'author', 'name', 2000),(1,'author', 'name', 2000),(3,'author', 'name', 2000),(1,'author', 'name', 2000),(1,'author', 'name', 2000),(5,'author', 'name', 2000),(1,'author', 'name', 2000),(1,'author', 'name', 2000),(1,'author', 'name', 2000),(1,'author', 'name', 2000),(1,'author', 'name', 2000),(1,'author', 'name', 2000)]

heads = ['id', 'author', 'name', 'year'] #столбики
table = ttk.Treeview(frametable, show = 'headings') #инициализация таблицы
table['columns'] = heads #привязка столбцов к таблице

for header in heads: #для каждого столбика выравниваем по центру все ячейки
    table.heading(header, text = header, anchor = 'center')
    table.column(header, anchor = 'center')

for row in lst: #для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
    table.insert('', tkinter.END, values = row) #без неё слева будет большой пропуст т к предуматривается полноценная иерархия

scroll_pane = ttk.Scrollbar(frametable, command=table.yview)
table.configure(yscrollcommand=scroll_pane.set)
scroll_pane.pack(side = tkinter.RIGHT,fill= tkinter.Y)
table.pack(expand = tkinter.YES, fill = tkinter.BOTH) #штука которая увеличивает таблицу в зависимости от кол-ва строк
