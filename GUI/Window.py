from tkinter import *
from tkinter.constants import NORMAL
from tkinter import messagebox, ttk
from tkinter.filedialog import asksaveasfilename
import tkinter, os
import tkinter.filedialog
from PIL import Image, ImageTk
from Parsing.Scopus import Scopus
from Parsing.Wos import Wos
from Parsing.iPublishing import IPublishing
from Parsing.eLibrary import eLibrary
from App.Equals import identical_sources_equals, different_source_equals
from App.Upload import Upload

win = Tk()

# списки со статьями
list_scopus = []
list_wos = []
list_elibrary = []
list_ipublishing = []

lst = []
list1 = []
list2 = []

left_table_create = False
right_table_create = False

left_table_site = ''
right_table_site = ''

add_new_list = []
remove_new_list = []
identical_new_list = []


def on_closing():
    if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
        win.destroy()


def sort(table, col, reverse):
    l = [(table.set(k, col), k) for k in table.get_children("")]
    l.sort(reverse=reverse)
    for index, (_, k) in enumerate(l):
        table.move(k, "", index)
    table.heading(col, command=lambda: sort(table, col, not reverse))


left_name_file = ""
right_name_file = ""


def open_file_Scopus_left():
    ftypes = [("xlsx", "*.xlsx"), ('All files', '*')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))
    filename = dlg.show()  # получение имени файла для дальнейшей работы

    global left_name_file
    temp = filename[::-1]
    temp2 = ""
    for i in range(0, len(temp)):
        if (temp[i] != '/'):
            temp2 += temp[i]
        else:
            break
    left_name_file = temp2[::-1]

    if len(filename) > 0:  # если не пустое имя файла
        # переменные чтоб понимать что было загружено в таблицу 'w' - WoS, 's' - Scopus, 'i' - iPublishing, 'e' - eLibrary
        global left_table_site, right_table_site
        global left_table_create
        global table_left
        global scroll_pane_left
        mainmenu.entryconfigure(2, state=DISABLED)
        left_table_site = 's'
        if ((left_table_site == 's' and right_table_site == 's') or
                (left_table_site == 'i' and right_table_site == 's') or
                (left_table_site == 's' and right_table_site == 'i')):
            mainmenu.entryconfigure(2, state=NORMAL)  # разблокирование кнопки сравнить данные
        if left_table_create == True:
            table_left.destroy()
            scroll_pane_left.pack_forget()
        # обработка файла, получение списка данных
        list_scopus = Scopus(filename)
        if list_scopus != None:
            lst = []
            name_left.configure(text=nameleft())
            for i in range(len(list_scopus)):
                lst.append((list_scopus[i].author, list_scopus[i].title, list_scopus[i].year, list_scopus[i].link,
                            list_scopus[i].citation))
            global list1
            list1 = list_scopus
            heads = ['author', 'title', 'year', 'link', 'citation']  # столбики
            table_left = ttk.Treeview(frametableleft, show='headings')  # инициализация таблицы
            table_left['columns'] = heads  # привязка столбцов к таблице
            left_table_create = True

            for header in heads:  # для каждого столбика выравниваем по центру все ячейки
                table_left.heading(header, text=header, anchor='center')
                table_left.column(header, anchor='center')

            scroll_pane_left = ttk.Scrollbar(frametableleft, command=(table_left.yview))
            table_left.configure(yscrollcommand=scroll_pane_left.set)
            scroll_pane_left.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            table_left.pack(expand=tkinter.YES,
                            fill=tkinter.BOTH)  # штука которая увеличивает таблицу в зависимости от кол-ва строк

            for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
                table_left.insert('', tkinter.END, values=row)

            table_left.column("author", minwidth=100, width=100, stretch=NO)
            table_left.column("title", minwidth=330, width=330, stretch=YES)
            table_left.column("year", minwidth=40, width=40, stretch=NO)
            table_left.column("link", minwidth=180, width=180, stretch=NO)
            table_left.column("citation", minwidth=60, width=60, stretch=NO)

            table_left.heading("author", text="author", command=lambda: sort(table_left, 0, False))
            table_left.heading("title", text="title", command=lambda: sort(table_left, 1, False))
            table_left.heading("year", text="year", command=lambda: sort(table_left, 2, False))
            table_left.heading("link", text="link", command=lambda: sort(table_left, 3, False))
            table_left.heading("citation", text="citation", command=lambda: sort(table_left, 4, False))
        else:
            tkinter.messagebox.showwarning(title="Предупреждение",
                                           message="Возможно Вы пытаетесь загрузить не Scopus, или файл повреждён, или не имеет строчек данных")


def open_file_Scopus_right():
    ftypes = [("xlsx", "*.xlsx"), ('All files', '*')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))
    filename = dlg.show()  # получение имени файла для дальнейшей работы

    global right_name_file
    temp = filename[::-1]
    temp2 = ""
    for i in range(0, len(temp)):
        if (temp[i] != '/'):
            temp2 += temp[i]
        else:
            break
    right_name_file = temp2[::-1]

    if len(filename) > 0:  # если не пустое имя файла
        # переменные чтоб понимать что было загружено в таблицу 'w' - WoS, 's' - Scopus, 'i' - iPublishing, 'e' - eLibrary
        global left_table_site, right_table_site
        global right_table_create
        global table_right
        global scroll_pane_right
        mainmenu.entryconfigure(2, state=DISABLED)
        right_table_site = 's'
        if ((left_table_site == 's' and right_table_site == 's') or
                (left_table_site == 'i' and right_table_site == 's') or
                (left_table_site == 's' and right_table_site == 'i')):
            mainmenu.entryconfigure(2, state=NORMAL)  # разблокирование кнопки сравнить данные
        # обработка файла, получение списка данных
        list_scopus = Scopus(filename)
        if right_table_create == True:
            table_right.destroy()
            scroll_pane_right.pack_forget()
        if list_scopus != None:
            lst = []
            name_right.configure(text=nameright())
            for i in range(len(list_scopus)):
                lst.append((list_scopus[i].author, list_scopus[i].title, list_scopus[i].year, list_scopus[i].link,
                            list_scopus[i].citation))
            global list2
            list2 = list_scopus
            heads = ['author', 'title', 'year', 'link', 'citation']  # столбики
            table_right = ttk.Treeview(frametableright, show='headings')  # инициализация таблицы
            table_right['columns'] = heads  # привязка столбцов к таблице
            right_table_create = True

            for header in heads:  # для каждого столбика выравниваем по центру все ячейки
                table_right.heading(header, text=header, anchor='center')
                table_right.column(header, anchor='center')

            scroll_pane_right = ttk.Scrollbar(frametableright, command=table_right.yview)
            table_right.configure(yscrollcommand=scroll_pane_right.set)
            scroll_pane_right.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            table_right.pack(expand=tkinter.YES, fill=tkinter.BOTH)

            for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
                table_right.insert('', tkinter.END, values=row)

            table_right.column("author", minwidth=100, width=100, stretch=NO)
            table_right.column("title", minwidth=330, width=330, stretch=YES)
            table_right.column("year", minwidth=40, width=40, stretch=NO)
            table_right.column("link", minwidth=180, width=180, stretch=NO)
            table_right.column("citation", minwidth=60, width=60, stretch=NO)

            table_right.heading("author", text="author", command=lambda: sort(table_right, 0, False))
            table_right.heading("title", text="title", command=lambda: sort(table_right, 1, False))
            table_right.heading("year", text="year", command=lambda: sort(table_right, 2, False))
            table_right.heading("link", text="link", command=lambda: sort(table_right, 3, False))
            table_right.heading("citation", text="citation", command=lambda: sort(table_right, 4, False))
        else:
            tkinter.messagebox.showwarning(title="Предупреждение",
                                           message="Возможно Вы пытаетесь загрузить не Scopus, или файл повреждён, или не имеет строчек данных")


def open_file_WoS_left():
    ftypes = [("xls", "*.xls?"), ('All files', '*')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))
    filename = dlg.show()  # получение имени файла для дальнейшей работы

    global left_name_file
    temp = filename[::-1]
    temp2 = ""
    for i in range(0, len(temp)):
        if (temp[i] != '/'):
            temp2 += temp[i]
        else:
            break
    left_name_file = temp2[::-1]

    if len(filename) > 0:  # если не пустое имя файла
        # переменные чтоб понимать что было загружено в таблицу 'w' - WoS, 's' - Scopus, 'i' - iPublishing, 'e' - eLibrary
        global left_table_site, right_table_site
        global left_table_create
        global table_left
        global scroll_pane_left
        mainmenu.entryconfigure(2, state=DISABLED)
        left_table_site = 'w'
        if ((left_table_site == 'w' and right_table_site == 'w') or
                (left_table_site == 'i' and right_table_site == 'w') or
                (left_table_site == 'w' and right_table_site == 'i')):
            mainmenu.entryconfigure(2, state=NORMAL)  # разблокирование кнопки сравнить данные
        if left_table_create == True:
            table_left.destroy()
            scroll_pane_left.pack_forget()
        # обработка файла, получение списка данных
        list_wos = Wos(filename)
        if list_wos != None:
            lst = []
            name_left.configure(text=nameleft())
            for i in range(len(list_wos)):
                lst.append((list_wos[i].author, list_wos[i].title, list_wos[i].year, list_wos[i].link))
            global list1
            list1 = list_wos

            heads = ['author', 'title', 'year', 'link']  # столбики
            table_left = ttk.Treeview(frametableleft, show='headings')  # инициализация таблицы
            table_left['columns'] = heads  # привязка столбцов к таблице
            left_table_create = True

            for header in heads:  # для каждого столбика выравниваем по центру все ячейки
                table_left.heading(header, text=header, anchor='center')
                table_left.column(header, anchor='center')

            scroll_pane_left = ttk.Scrollbar(frametableleft, command=table_left.yview)
            table_left.configure(yscrollcommand=scroll_pane_left.set)
            scroll_pane_left.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            table_left.pack(expand=tkinter.YES, fill=tkinter.BOTH)

            for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
                table_left.insert('', tkinter.END, values=row)

            table_left.column("author", minwidth=100, width=100, stretch=NO)
            table_left.column("title", minwidth=330, width=330, stretch=YES)
            table_left.column("year", minwidth=40, width=40, stretch=NO)
            table_left.column("link", minwidth=180, width=180, stretch=NO)

            table_left.heading("author", text="author", command=lambda: sort(table_left, 0, False))
            table_left.heading("title", text="title", command=lambda: sort(table_left, 1, False))
            table_left.heading("year", text="year", command=lambda: sort(table_left, 2, False))
            table_left.heading("link", text="link", command=lambda: sort(table_left, 3, False))
        else:
            tkinter.messagebox.showwarning(title="Предупреждение",
                                           message="Возможно Вы пытаетесь загрузить не Wos, или файл повреждён, или не имеет строчек данных")


def open_file_WoS_right():
    ftypes = [("xls", "*.xls?"), ('All files', '*')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))
    filename = dlg.show()  # получение имени файла для дальнейшей работы

    global right_name_file
    temp = filename[::-1]
    temp2 = ""
    for i in range(0, len(temp)):
        if (temp[i] != '/'):
            temp2 += temp[i]
        else:
            break
    right_name_file = temp2[::-1]

    if len(filename) > 0:  # если не пустое имя файла
        # переменные чтоб понимать что было загружено в таблицу 'w' - WoS, 's' - Scopus, 'i' - iPublishing, 'e' - eLibrary
        global left_table_site, right_table_site
        global right_table_create
        global table_right
        global scroll_pane_right
        mainmenu.entryconfigure(2, state=DISABLED)
        right_table_site = 'w'
        if ((left_table_site == 'w' and right_table_site == 'w') or
                (left_table_site == 'i' and right_table_site == 'w') or
                (left_table_site == 'w' and right_table_site == 'i')):
            mainmenu.entryconfigure(2, state=NORMAL)  # разблокирование кнопки сравнить данные
        # обработка файла, получение списка данных
        list_wos = Wos(filename)
        if right_table_create == True:
            table_right.destroy()
            scroll_pane_right.pack_forget()

        if list_wos != None:
            lst = []
            name_right.configure(text=nameright())
            for i in range(len(list_wos)):
                lst.append((list_wos[i].author, list_wos[i].title, list_wos[i].year, list_wos[i].link))
            global list2
            list2 = list_wos
            heads = ['author', 'title', 'year', 'link']  # столбики
            table_right = ttk.Treeview(frametableright, show='headings')  # инициализация таблицы
            table_right['columns'] = heads  # привязка столбцов к таблице
            right_table_create = True

            for header in heads:  # для каждого столбика выравниваем по центру все ячейки
                table_right.heading(header, text=header, anchor='center')
                table_right.column(header, anchor='center')

            scroll_pane_right = ttk.Scrollbar(frametableright, command=table_right.yview)
            table_right.configure(yscrollcommand=scroll_pane_right.set)
            scroll_pane_right.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            table_right.pack(expand=tkinter.YES, fill=tkinter.BOTH)

            for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
                table_right.insert('', tkinter.END, values=row)

            table_right.column("author", minwidth=100, width=100, stretch=NO)
            table_right.column("title", minwidth=330, width=330, stretch=YES)
            table_right.column("year", minwidth=40, width=40, stretch=NO)
            table_right.column("link", minwidth=180, width=180, stretch=NO)

            table_right.heading("author", text="author", command=lambda: sort(table_right, 0, False))
            table_right.heading("title", text="title", command=lambda: sort(table_right, 1, False))
            table_right.heading("year", text="year", command=lambda: sort(table_right, 2, False))
            table_right.heading("link", text="link", command=lambda: sort(table_right, 3, False))
        else:
            tkinter.messagebox.showwarning(title="Предупреждение",
                                           message="Возможно Вы пытаетесь загрузить не Wos, или файл повреждён, или не имеет строчек данных")


def open_file_Elibrary_left():
    ftypes = [("xml", "*.xml"), ('All files', '*')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))
    filename = dlg.show()  # получение имени файла для дальнейшей работы

    global left_name_file
    temp = filename[::-1]
    temp2 = ""
    for i in range(0, len(temp)):
        if (temp[i] != '/'):
            temp2 += temp[i]
        else:
            break
    left_name_file = temp2[::-1]

    if len(filename) > 0:  # если не пустое имя файла
        # переменные чтоб понимать что было загружено в таблицу 'w' - WoS, 's' - Scopus, 'i' - iPublishing, 'e' - eLibrary
        global left_table_site, right_table_site
        global left_table_create
        global table_left
        global scroll_pane_left
        mainmenu.entryconfigure(2, state=DISABLED)
        left_table_site = 'e'
        if ((left_table_site == 'e' and right_table_site == 'e') or
                (left_table_site == 'i' and right_table_site == 'e') or
                (left_table_site == 'e' and right_table_site == 'i')):
            mainmenu.entryconfigure(2, state=NORMAL)  # разблокирование кнопки сравнить данные
        if left_table_create == True:
            table_left.destroy()
            scroll_pane_left.pack_forget()
        # обработка файла, получение списка данных
        list_Elibrary = eLibrary(filename)
        if list_Elibrary != None:
            lst = []
            name_left.configure(text=nameleft())
            for i in range(len(list_Elibrary)):
                lst.append(
                    (list_Elibrary[i].author, list_Elibrary[i].title, list_Elibrary[i].year, list_Elibrary[i].link))
            global list1
            list1 = list_Elibrary
            heads = ['author', 'title', 'year', 'link']  # столбики
            table_left = ttk.Treeview(frametableleft, show='headings')  # инициализация таблицы
            table_left['columns'] = heads  # привязка столбцов к таблице
            left_table_create = True

            for header in heads:  # для каждого столбика выравниваем по центру все ячейки
                table_left.heading(header, text=header, anchor='center')
                table_left.column(header, anchor='center')

            scroll_pane_left = ttk.Scrollbar(frametableleft, command=table_left.yview)
            table_left.configure(yscrollcommand=scroll_pane_left.set)
            scroll_pane_left.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            table_left.pack(expand=tkinter.YES, fill=tkinter.BOTH)

            for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
                table_left.insert('', tkinter.END, values=row)

            table_left.column("author", minwidth=100, width=100, stretch=NO)
            table_left.column("title", minwidth=370, width=370, stretch=YES)
            table_left.column("year", minwidth=40, width=40, stretch=NO)
            table_left.column("link", minwidth=210, width=210, stretch=NO)

            table_left.heading("author", text="author", command=lambda: sort(table_left, 0, False))
            table_left.heading("title", text="title", command=lambda: sort(table_left, 1, False))
            table_left.heading("year", text="year", command=lambda: sort(table_left, 2, False))
            table_left.heading("link", text="link", command=lambda: sort(table_left, 3, False))
        else:
            tkinter.messagebox.showwarning(title="Предупреждение",
                                           message="Возможно Вы пытаетесь загрузить не eLibrary, или файл повреждён, или не имеет строчек данных")


def open_file_Elibrary_right():
    ftypes = [("xml", "*.xml"), ('All files', '*')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))
    filename = dlg.show()  # получение имени файла для дальнейшей работы

    global right_name_file
    temp = filename[::-1]
    temp2 = ""
    for i in range(0, len(temp)):
        if (temp[i] != '/'):
            temp2 += temp[i]
        else:
            break
    right_name_file = temp2[::-1]

    if len(filename) > 0:  # если не пустое имя файла
        # переменные чтоб понимать что было загружено в таблицу 'w' - WoS, 's' - Scopus, 'i' - iPublishing, 'e' - eLibrary
        global left_table_site, right_table_site
        global right_table_create
        global table_right
        global scroll_pane_right
        mainmenu.entryconfigure(2, state=DISABLED)
        right_table_site = 'e'
        if ((left_table_site == 'e' and right_table_site == 'e') or
                (left_table_site == 'i' and right_table_site == 'e') or
                (left_table_site == 'e' and right_table_site == 'i')):
            mainmenu.entryconfigure(2, state=NORMAL)  # разблокирование кнопки сравнить данные
        # обработка файла, получение списка данных
        list_Elibrary = eLibrary(filename)
        if right_table_create == True:
            table_right.destroy()
            scroll_pane_right.pack_forget()

        if list_Elibrary != None:
            lst = []
            name_right.configure(text=nameright())
            for i in range(len(list_Elibrary)):
                lst.append(
                    (list_Elibrary[i].author, list_Elibrary[i].title, list_Elibrary[i].year, list_Elibrary[i].link))
            global list2
            list2 = list_Elibrary
            heads = ['author', 'title', 'year', 'link']  # столбики
            table_right = ttk.Treeview(frametableright, show='headings')  # инициализация таблицы
            table_right['columns'] = heads  # привязка столбцов к таблице
            right_table_create = True

            for header in heads:  # для каждого столбика выравниваем по центру все ячейки
                table_right.heading(header, text=header, anchor='center')
                table_right.column(header, anchor='center')

            scroll_pane_right = ttk.Scrollbar(frametableright, command=table_right.yview)
            table_right.configure(yscrollcommand=scroll_pane_right.set)
            scroll_pane_right.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            table_right.pack(expand=tkinter.YES, fill=tkinter.BOTH)

            for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
                table_right.insert('', tkinter.END, values=row)

            table_right.column("author", minwidth=100, width=100, stretch=NO)
            table_right.column("title", minwidth=370, width=370, stretch=YES)
            table_right.column("year", minwidth=40, width=40, stretch=NO)
            table_right.column("link", minwidth=210, width=210, stretch=NO)

            table_right.heading("author", text="author", command=lambda: sort(table_right, 0, False))
            table_right.heading("title", text="title", command=lambda: sort(table_right, 1, False))
            table_right.heading("year", text="year", command=lambda: sort(table_right, 2, False))
            table_right.heading("link", text="link", command=lambda: sort(table_right, 3, False))
        else:
            tkinter.messagebox.showwarning(title="Предупреждение",
                                           message="Возможно Вы пытаетесь загрузить не eLibrary, или файл повреждён, или не имеет строчек данных")


def open_file_Ipublishing_left():
    ftypes = [("xlsx", "*.xlsx"), ('All files', '*')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))
    filename = dlg.show()  # получение имени файла для дальнейшей работы

    global left_name_file
    temp = filename[::-1]
    temp2 = ""
    for i in range(0, len(temp)):
        if (temp[i] != '/'):
            temp2 += temp[i]
        else:
            break
    left_name_file = temp2[::-1]

    if len(filename) > 0:  # если не пустое имя файла
        # переменные чтоб понимать что было загружено в таблицу 'w' - WoS, 's' - Scopus, 'i' - iPublishing, 'e' - eLibrary
        global left_table_site, right_table_site
        global left_table_create
        global table_left
        global scroll_pane_left
        mainmenu.entryconfigure(2, state=DISABLED)
        left_table_site = 'i'
        if ((left_table_site == 'i' and right_table_site == 'w') or
                (left_table_site == 'i' and right_table_site == 's') or
                (left_table_site == 'i' and right_table_site == 'e') or
                (left_table_site == 'i' and right_table_site == 'i')):
            mainmenu.entryconfigure(2, state=NORMAL)  # разблокирование кнопки сравнить данные
        list_ipublishing = IPublishing(filename)
        if left_table_create == True:
            table_left.destroy()
            scroll_pane_left.pack_forget()

        if list_ipublishing != None:
            lst = []
            name_left.configure(text=nameleft())
            for i in range(len(list_ipublishing)):
                lst.append((list_ipublishing[i].author, list_ipublishing[i].title, list_ipublishing[i].year,
                            list_ipublishing[i].link))
            global list1
            list1 = list_ipublishing
            heads = ['author', 'title', 'year', 'link']  # столбики
            table_left = ttk.Treeview(frametableleft, show='headings')  # инициализация таблицы
            table_left['columns'] = heads  # привязка столбцов к таблице
            left_table_create = True

            for header in heads:  # для каждого столбика выравниваем по центру все ячейки
                table_left.heading(header, text=header, anchor='center')
                table_left.column(header, anchor='center')

            scroll_pane_left = ttk.Scrollbar(frametableleft, command=table_left.yview)
            table_left.configure(yscrollcommand=scroll_pane_left.set)
            scroll_pane_left.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            table_left.pack(expand=tkinter.YES, fill=tkinter.BOTH)

            for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
                table_left.insert('', tkinter.END, values=row)

            table_left.column("author", minwidth=100, width=100, stretch=NO)
            table_left.column("title", minwidth=250, width=250, stretch=YES)
            table_left.column("year", minwidth=40, width=40, stretch=NO)
            table_left.column("link", minwidth=160, width=160, stretch=NO)

            table_left.heading("author", text="author", command=lambda: sort(table_left, 0, False))
            table_left.heading("title", text="title", command=lambda: sort(table_left, 1, False))
            table_left.heading("year", text="year", command=lambda: sort(table_left, 2, False))
            table_left.heading("link", text="link", command=lambda: sort(table_left, 3, False))
        else:
            tkinter.messagebox.showwarning(title="Предупреждение",
                                           message="Возможно Вы пытаетесь загрузить не IPublishing, или файл повреждён, или не имеет строчек данных")


def open_file_Ipublishing_right():
    ftypes = [("xlsx", "*.xlsx"), ('All files', '*')]  # допустимые типы
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=os.path.abspath(__file__))
    filename = dlg.show()  # получение имени файла для дальнейшей работы

    global right_name_file
    temp = filename[::-1]
    temp2 = ""
    for i in range(0, len(temp)):
        if (temp[i] != '/'):
            temp2 += temp[i]
        else:
            break
    right_name_file = temp2[::-1]

    if len(filename) > 0:  # если не пустое имя файла
        # переменные чтоб понимать что было загружено в таблицу 'w' - WoS, 's' - Scopus, 'i' - iPublishing, 'e' - eLibrary
        global left_table_site, right_table_site
        global right_table_create
        global table_right
        global scroll_pane_right
        mainmenu.entryconfigure(2, state=DISABLED)
        right_table_site = 'i'
        if ((right_table_site == 'i' and left_table_site == 'w') or
                (right_table_site == 'i' and left_table_site == 's') or
                (right_table_site == 'i' and left_table_site == 'e') or
                (right_table_site == 'i' and left_table_site == 'i')):
            mainmenu.entryconfigure(2, state=NORMAL)  # разблокирование кнопки сравнить данные
        list_ipublishing = IPublishing(filename)
        if right_table_create == True:
            table_right.destroy()
            scroll_pane_right.pack_forget()

        if list_ipublishing != None:
            lst = []
            name_right.configure(text=nameright())
            for i in range(len(list_ipublishing)):
                lst.append((list_ipublishing[i].author, list_ipublishing[i].title, list_ipublishing[i].year,
                            list_ipublishing[i].link))
            global list2
            list2 = list_ipublishing
            heads = ['author', 'title', 'year', 'link']  # столбики
            table_right = ttk.Treeview(frametableright, show='headings')  # инициализация таблицы
            table_right['columns'] = heads  # привязка столбцов к таблице
            right_table_create = True

            for header in heads:  # для каждого столбика выравниваем по центру все ячейки
                table_right.heading(header, text=header, anchor='center')
                table_right.column(header, anchor='center')

            scroll_pane_right = ttk.Scrollbar(frametableright, command=table_right.yview)
            table_right.configure(yscrollcommand=scroll_pane_right.set)
            scroll_pane_right.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            table_right.pack(expand=tkinter.YES, fill=tkinter.BOTH)

            for row in lst:  # для каждой строки указываем что нет родителя (обязательная тема чтоб было красиво)
                table_right.insert('', tkinter.END, values=row)

            table_right.column("author", minwidth=100, width=100, stretch=NO)
            table_right.column("title", minwidth=250, width=250, stretch=YES)
            table_right.column("year", minwidth=40, width=40, stretch=NO)
            table_right.column("link", minwidth=160, width=160, stretch=NO)

            table_right.heading("author", text="author", command=lambda: sort(table_right, 0, False))
            table_right.heading("title", text="title", command=lambda: sort(table_right, 1, False))
            table_right.heading("year", text="year", command=lambda: sort(table_right, 2, False))
            table_right.heading("link", text="link", command=lambda: sort(table_right, 3, False))
        else:
            tkinter.messagebox.showwarning(title="Предупреждение",
                                           message="Возможно Вы пытаетесь загрузить не IPublishing, или файл повреждён, или не имеет строчек данных")


# кнопка сравнения
comparewin_is_open = False


def open_compare_window():
    global comparewin_is_open
    global comparewin
    global add_new_list
    global remove_new_list
    global identical_new_list
    if comparewin_is_open == True:
        comparewin.destroy()
    comparewin_is_open = True
    comparewin = Toplevel(win)  # инициализация
    comparewin.geometry('750x700')  # размер
    comparewin.minsize(750, 700)
    comparewin.title("Результат сравнения")  # название
    frame_compare_button = Frame(comparewin)  # задаем поле
    frame_compare_table = Frame(comparewin)  # задаем поле
    frame_compare_button.place(relx=0, rely=0, relwidth=1, relheight=0.1)  # размещаем его на весь размер окна
    frame_compare_table.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)  # размещаем его на весь размер окна

    heads = ['author', 'title', 'year', 'link']  # столбики
    table_compare = ttk.Treeview(frame_compare_table, show='headings')  # инициализация таблицы
    table_compare.place(relx=0, rely=0, relwidth=1, relheight=1)
    table_compare['columns'] = heads  # привязка столбцов к таблице

    for header in heads:  # для каждого столбика выравниваем по центру все ячейки
        table_compare.heading(header, text=header, anchor='center')
        table_compare.column(header, anchor='center')

    scroll_pane_compare = ttk.Scrollbar(frame_compare_table, command=(table_compare.yview))
    table_compare.configure(yscrollcommand=scroll_pane_compare.set)
    scroll_pane_compare.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    table_compare.pack(expand=tkinter.YES, fill=tkinter.BOTH)

    if left_table_site == right_table_site:
        list_new_tuple, list_ident_tuple, list_remove_tuple, add_new_list, identical_new_list, remove_new_list = identical_sources_equals(
            list1, list2)
    else:
        list_new_tuple, list_ident_tuple, list_remove_tuple, add_new_list, identical_new_list, remove_new_list = different_source_equals(
            list1, list2)

    unload_to_xlsx = Button(frame_compare_button, text="Выгрузить в таблицу xlsx", command=upload)
    unload_to_xlsx.place(relx=0.05, rely=0.25, relwidth=0.9, relheight=0.5)

    for row in list_new_tuple:
        table_compare.insert('', tkinter.END, values=row, tags='new')
    for row in list_ident_tuple:
        table_compare.insert('', tkinter.END, values=row, tags='edited')
    for row in list_remove_tuple:
        table_compare.insert('', tkinter.END, values=row, tags='deleted')

    table_compare.tag_configure('new', background='#7FFF00')
    table_compare.tag_configure('deleted', background='#F08080')
    table_compare.tag_configure('edited', background='white')

    table_compare.column("author", minwidth=100, width=100, stretch=NO)
    table_compare.column("title", minwidth=370, width=370, stretch=YES)
    table_compare.column("year", minwidth=40, width=40, stretch=NO)
    table_compare.column("link", minwidth=210, width=210, stretch=NO)

    table_compare.heading("author", text="author", command=lambda: sort(table_compare, 0, False))
    table_compare.heading("title", text="title", command=lambda: sort(table_compare, 1, False))
    table_compare.heading("year", text="year", command=lambda: sort(table_compare, 2, False))
    table_compare.heading("link", text="link", command=lambda: sort(table_compare, 3, False))


photo = "global"
help_is_open = False


def help_guide():
    global help_is_open
    global helpwin
    global photo
    if help_is_open == True:
        helpwin.destroy()
    help_is_open = True
    helpwin = Toplevel(win)  # инициализация
    helpwin.geometry('800x800')  # размер
    helpwin.resizable(False, False)
    helpwin.title("Окно помощи")  # название
    frame_help = Frame(helpwin)  # задаем поле
    frame_help.place(relx=0, rely=0, relwidth=1, relheight=1)  # размещаем его на весь размер окна
    photo = ImageTk.PhotoImage(Image.open("help.jpg"))
    label_help = tkinter.Label(frame_help, image=photo)  # задаем поле
    label_help.place(relx=0, rely=0, relwidth=1, relheight=1)  # размещаем его на весь размер окна


def upload():
    global add_new_list
    global remove_new_list
    global identical_new_list
    path = asksaveasfilename(initialfile='DefaultName.xlsx', defaultextension=".xlsx", filetypes=[("xlsx", "*.xlsx")])
    if len(path) > 0:
        Upload(path, add_new_list, identical_new_list, remove_new_list)
        tkinter.messagebox.showwarning(title="Оповещение", message="Данные успешно выгружены в excel")


def nameleft():
    global left_table_site
    if left_table_site == '':
        return ""
    else:
        return left_name_file


def nameright():
    global right_table_site
    if right_table_site == '':
        return ""
    else:
        return right_name_file


# создание окна
win['bg'] = '#FFFFFF'  # цвет
win.title('Library')  # название
win.geometry('1500x700')  # размер
win.protocol("WM_DELETE_WINDOW", on_closing)  # событие при закрытии приложения
win.minsize(1500, 700)

# блоки основного окна
framenameleft = Frame(win, bg='#FFFFFF')
framenameright = Frame(win, bg='#FFFFFF')

frametableleft = Frame(win, bg='#FFFFFF')
frametableright = Frame(win, bg='#FFFFFF')

# расположение блоков, чтоб можно было менять размер окна
framenameleft.place(relx=0, rely=0, relwidth=0.5, relheight=0.04)
framenameright.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.04)

frametableleft.place(relx=0, rely=0.04, relwidth=0.5, relheight=1)
frametableright.place(relx=0.5, rely=0.04, relwidth=0.5, relheight=1)

name_left = tkinter.Label(framenameleft, text=nameleft(), background='#FFFFFF')
name_right = tkinter.Label(framenameright, text=nameright(), background='#FFFFFF')

name_left.place(relx=0.25, rely=0, relwidth=0.5, relheight=1)
name_right.place(relx=0.25, rely=0, relwidth=0.5, relheight=1)

# меню
mainmenu = Menu(win)
win.config(menu=mainmenu)

# создание самого меню
filemenu = Menu(mainmenu, tearoff=0)

# создание поля загрузка файлов
filemenu_load = Menu(filemenu, tearoff=0)

filemenu_load_WoF = Menu(filemenu_load, tearoff=0)
filemenu_load_WoF.add_command(label="Загрузить в левую таблицу", command=(open_file_WoS_left))
filemenu_load_WoF.add_command(label="Загрузить в правую таблицу", command=(open_file_WoS_right))
filemenu_load.add_cascade(label="Загрузить Web of Science", menu=filemenu_load_WoF)

filemenu_load_Scopus = Menu(filemenu_load, tearoff=0)
filemenu_load_Scopus.add_command(label="Загрузить в левую таблицу", command=(open_file_Scopus_left))
filemenu_load_Scopus.add_command(label="Загрузить в правую таблицу", command=(open_file_Scopus_right))
filemenu_load.add_cascade(label="Загрузить Scopus", menu=filemenu_load_Scopus)

filemenu_load_Elibrary = Menu(filemenu_load, tearoff=0)
filemenu_load_Elibrary.add_command(label="Загрузить в левую таблицу", command=(open_file_Elibrary_left))
filemenu_load_Elibrary.add_command(label="Загрузить в правую таблицу", command=(open_file_Elibrary_right))
filemenu_load.add_cascade(label="Загрузить Elibrary", menu=filemenu_load_Elibrary)

filemenu_load_Ipublishing = Menu(filemenu_load, tearoff=0)
filemenu_load_Ipublishing.add_command(label="Загрузить в левую таблицу", command=(open_file_Ipublishing_left))
filemenu_load_Ipublishing.add_command(label="Загрузить в правую таблицу", command=(open_file_Ipublishing_right))
filemenu_load.add_cascade(label="Загрузить Ipublishing", menu=filemenu_load_Ipublishing)

# создание главных полей
mainmenu.add_cascade(label="Загрузить файл", menu=filemenu_load)
mainmenu.add_cascade(label="Сравнить данные", command=(open_compare_window), state=DISABLED)
mainmenu.add_cascade(label="Помощь", command=(help_guide))