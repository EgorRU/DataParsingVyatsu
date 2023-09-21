from tkinter import ttk, Tk
import tkinter.filedialog
import tkinter
import os

pid = os.getpid()
with open("pid.txt", 'w') as file:
    file.write(str(pid))

loading_win = Tk()
loading_win['bg'] = '#FFFFFF'  # цвет
loading_win.title('Load')  # название
loading_win.geometry('200x200')  # размер
loading_win.resizable(False, False)

progressbar = ttk.Progressbar(loading_win, orient="horizontal", mode="indeterminate")
progressbar.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.1)
progressbar.start(30)  # запускаем progressbar

label = tkinter.Label(loading_win, text="Пожалуйста, подождите")
label.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.2)
loading_win.mainloop()