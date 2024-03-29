# -*- coding: utf-8 -*-
######################
# Skype: xkcd..
# Python version: 2.7
######################
__author__ = 'Dmitry Kryukov'
__version__ = "1.0.0"
__email__ = "remasik@gmail.com"
__status__ = "Test"

"""
    Transliterate text from file
"""

from Tkinter import *
from tkFileDialog import *
import ttk
import sys
import transliterate


class Encoder:
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
        self.txt.insert(END, 'Выберите .txt файл.')

        buttOpen = ttk.Button(root, command=self.file_open, text='Выбрать файл...')
        buttSave = ttk.Button(root, command=self.file_save, text='Кодировать')
        buttOpen.pack(side = 'left')
        buttSave.pack(side = 'left')

        # Форматы для отображения среди файлов
        self.myFormats = [('TXT','*.txt'),]
        self.defaultextension = '.txt'

    def _exit(self):
        root.destroy()
        sys.exit()

    def _help(self):
        help = Tk()
        txt = Text(help,width=75,height=20,background='gray95', font=('times',12),wrap=WORD)
        txt.pack(expand=YES,fill=BOTH)
        txt.insert(END, 'Программа транслитерирует текст из txt файла.')
        #установка тегов для областей текста
        txt.tag_add('title','1.0','1.end')
        #конфигурирование тегов
        txt.tag_config('title', foreground='red', font=('times',14,'underline'),justify=CENTER)
        help.mainloop()

    def file_open(self):
        fileName = askopenfilename(parent=root, filetypes=self.myFormats, initialdir='C:\Users', title="Открыть файл для декодирования...")
        if len(fileName ) > 0:
            self.txt.delete('1.0',END)
            self.txt.insert(END, 'Файл загружен успешно!')
            with open(fileName) as f:
                self.encoded = f.read()
        else:
            self.txt.delete('1.0',END)
            self.txt.insert(END, 'Файл не загрузился. Ошибка!')
            self.txt.tag_add('title','1.0','1.end')
            self.txt.tag_config('title', foreground='red', font=('courier new',10))

    def file_save(self):
        encoded = self.encoded
        if len(encoded) > 1:
            self.txt.delete('1.0',END)
            try:
                encoded = encoded.decode('utf-8')
            except UnicodeDecodeError:
                self.txt.insert(END, 'Файл уже декодирован!')
                self.txt.tag_add('title','1.0','1.end')
                self.txt.tag_config('title', foreground='red', font=('courier new',10))
            replacers = [u'»',
                         u'«',]
            for x in replacers:
                encoded = encoded.replace(x, '"')
            fileName = asksaveasfilename(parent=root, initialdir='C:\Users',defaultextension=self.defaultextension, title="Сохранить файл...")
            try:
                with open(fileName,"w") as f:
                    #f.write(encoded.encode('cp1251'))
					f.write(transliterate.translit(encoded, 'ru', reversed=True))
                self.txt.insert(END, u'Файл %s успешно сохранен!' % fileName.split('/')[-1])
            except UnicodeEncodeError as error:
                self.txt.insert(END, u'Ошибка кодирования!')
                self.txt.tag_add('title','1.0','1.end')
                self.txt.tag_config('title', foreground='red', font=('courier new',10))
                err = Tk()
                err.title('Ошибка!')
                err_txt = Text(err,width=75,height=20,background='gray95', font=('times',12),wrap=WORD)
                err_txt.pack(expand=YES,fill=BOTH)
                err_txt.insert(END, 'Данную информацию нужно отправить разработчику!\n\n')
                err_txt.insert(END, error)
                err_txt.tag_add('title','1.0','1.end')
                err_txt.tag_config('title', foreground='red', font=('times',12,'underline'),justify=CENTER)
                err.mainloop()

root = Tk()
root.title("All_translit v.1.0")
# на весь экран
#root.wm_state('zoomed')
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.wm_geometry("+%d+%d" % (x, y))
obj_menu = Encoder()
root.mainloop()



# with open(r'C:\Users\PK-DPI-742\Desktop\lst.txt', 'w') as f:
# 	f.write(transliterate.translit(text, 'ru', reversed=True))