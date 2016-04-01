# coding: utf-8
__author__ = 'Dmitry Kryukov'
__email__ = "remasik@gmail.com"


from Tkinter import *
from tkFileDialog import *
import ttk
import sys
import re
import os


class YamlIdDoubles:
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
        self.txt.insert(END, 'Выберите файл.')

        buttOpen = ttk.Button(root, command=self.file_open, text='Выбрать файл...')
        buttSave = ttk.Button(root, command=self.file_save, text='Обработать')
        buttOpen.pack(side = 'left')
        buttSave.pack(side = 'left')

        # Форматы для отображения среди файлов
        self.myFormats = [('YAML','*.yaml'),
                          ]
        self.defaultextension = '.yaml'

    def _exit(self):
        root.destroy()
        sys.exit()

    def _help(self):
        help = Tk()
        txt = Text(help,width=75,height=20,background='gray95', font=('times',12),wrap=WORD)
        txt.pack(expand=YES,fill=BOTH)
        txt.insert(END, 'Программа ищет дубликаты id в yaml файлах.\n')
        #установка тегов для областей текста
        txt.tag_add('title','1.0','1.end')
        #конфигурирование тегов
        txt.tag_config('title', foreground='red', font=('times',14,'underline'),justify=CENTER)
        help.mainloop()

    def file_open(self):
        fileName = askopenfilename(parent=root, filetypes=self.myFormats, initialdir='C:\Users', title="Открыть файл для обработки...")
        self.fileName = fileName
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
        if os.path.exists('log.txt'):
            try:
                os.remove('log.txt')
            except:
                raise
        if len(encoded) > 1:
            id = re.findall('imscc_identifier: \S+', encoded)
            uniq_id = dict()
            for x in id:
                if x in uniq_id.keys():
                    uniq_id[x] = uniq_id[x]+1
                else:
                    uniq_id[x] = 1
            res = Tk()
            res.title('Результат!')
            res_txt = Text(res,width=75,height=20,background='gray95', font=('times',12),wrap=WORD)
            res_txt.pack(expand=YES,fill=BOTH)
            for x,v in uniq_id.items():
                res_txt.insert(END, v)
                res_txt.insert(END, ' - '+x)
                res_txt.insert(END, '\n')
            with open('log.txt', 'w') as f:
                for x,v in uniq_id.items():
                    f.write('%s - %s \n' % (v,x))
            res.mainloop()


root = Tk()
root.title("YamlIdDoubles v.1.0")
# на весь экран
#root.wm_state('zoomed')
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.wm_geometry("+%d+%d" % (x, y))
obj_menu = YamlIdDoubles()
root.mainloop()