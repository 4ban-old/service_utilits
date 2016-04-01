# coding: utf-8
__author__ = 'Dmitry Kryukov'
__email__ = "remasik@gmail.com"


from Tkinter import *
from tkFileDialog import *
import ttk
import sys
import re
import os


class XmlMerge:
    def __init__(self):
        # главное меню
        menu = Menu(root)
        root.config(menu=menu)
        # Выпадающие менюшки
        appFile = Menu(menu)
        appHelp = Menu(menu)
        # Добавление событий в выпадающие менюшки
        appFile.add_command(label="Выход",command=self._exit)
        appHelp.add_command(label="Помощь",command=self._help)
        # Привязка выпадающих менюшек к кнопкам на главном меню
        menu.add_cascade(label="Файл",menu=appFile)
        menu.add_cascade(label="Помощь",menu=appHelp)

        self.txt = Text(root,width=40,height=1,font=('courier new',10), background='gray95', wrap=WORD)
        self.txt.pack(expand=YES,fill=BOTH)
        self.txt.insert(END, 'Выберите файлы для слияния.')

        buttOpen1 = ttk.Button(root, command=self.file_open1, text='Выбрать файл lms.xml')
        buttOpen2 = ttk.Button(root, command=self.file_open2, text='Выбрать файл canvas.xml')
        buttSave = ttk.Button(root, command=self.file_save, text='Обработать')
        buttOpen1.pack(side = 'left')
        buttOpen2.pack(side = 'left')
        buttSave.pack(side = 'left')

        # Форматы для отображения среди файлов
        self.myFormats = [('XML','*.xml'),
                          ]
        self.defaultextension = '.xml'

    def _exit(self):
        root.destroy()
        sys.exit()

    def _help(self):
        help = Tk()
        txt = Text(help,width=75,height=20,background='gray95', font=('times',12),wrap=WORD)
        txt.pack(expand=YES,fill=BOTH)
        txt.insert(END, 'Программа для слияния двух xml файлов.\n')
        #установка тегов для областей текста
        txt.tag_add('title','1.0','1.end')
        #конфигурирование тегов
        txt.tag_config('title', foreground='red', font=('times',14,'underline'),justify=CENTER)
        help.mainloop()

    def file_open1(self):
        fileName = askopenfilename(parent=root, filetypes=self.myFormats, initialdir='C:\Users', title="Открыть файл для обработки...")
        self.lms_name = fileName
        if len(fileName ) > 0:
            self.txt.delete('1.0',END)
            self.txt.insert(END, 'Файл загружен успешно!')
            with open(fileName) as f:
                self.lms = f.read()
        else:
            self.txt.delete('1.0',END)
            self.txt.insert(END, 'Файл не загрузился. Ошибка!')
            self.txt.tag_add('title','1.0','1.end')
            self.txt.tag_config('title', foreground='red', font=('courier new',10))

    def file_open2(self):
        fileName = askopenfilename(parent=root, filetypes=self.myFormats, initialdir='C:\Users', title="Открыть файл для обработки...")
        self.canvas_name = fileName
        if len(fileName ) > 0:
            self.txt.delete('1.0',END)
            self.txt.insert(END, 'Файл загружен успешно!')
            with open(fileName) as f:
                self.canvas = f.read()
        else:
            self.txt.delete('1.0',END)
            self.txt.insert(END, 'Файл не загрузился. Ошибка!')
            self.txt.tag_add('title','1.0','1.end')
            self.txt.tag_config('title', foreground='red', font=('courier new',10))

    def file_save(self):
        lms_name = self.lms_name
        canvas_name = self.canvas_name
        lms = self.lms
        canvas = self.canvas
        if os.path.exists('log.txt'):
            try:
                os.remove('log.txt')
            except:
                raise
        print lms_name
        print canvas_name
        print lms
        print canvas
        self._exit()


root = Tk()
root.title("XML merge tool v.1.0")
# на весь экран
#root.wm_state('zoomed')
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.wm_geometry("+%d+%d" % (x, y))
obj_menu = XmlMerge()
root.mainloop()