# -*- coding: utf-8 -*-
__author__ = 'Dmitry Kryukov'
__email__ = "remasik@gmail.com"

import os
import re
import logging
import transliterate
import ttk
from tkinter import *
import copy


class Logic:
    def __init__(self, targets):
        self.targets = targets
        target_counter = 0
        # Проход по папкам
        for target in self.targets:
            target_counter += 1
            res = target+r'\res'
            if not os.path.exists(res):
                try:
                    os.mkdir(res)
                    print ('>>> Папка res в  %s создана.' % target)
                except:
                    raise

            if os.path.exists(target+r'\res\_blah_log'+str(target_counter)+'.html'):
                try:
                    os.remove(target+r'\res\_blah_log'+str(target_counter)+'.html')
                except:
                    raise

            logger = logging.getLogger(target+'\\res\\'+str(target_counter))
            logger.addHandler(logging.FileHandler(target+'\\res\_blah_log'+str(target_counter)+'.html'))
            self.log = logging.getLogger(target+'\\res\\'+str(target_counter))
            self.log.warning('<html><head>'
                             '<meta charset="windows-1251">'
                             '<style type="text/css">'
                             '.res{ width:100%; background-color: #eeeeee; border-width:1px; color: #232323; cellpadding: 5px; font-family: courier new; font-size: 12px;}'
                             '.tab{max-width:100%;}'
                             '.tab2{max-width:50%;}'
                             '.text{color:#e4e4e4;}'
                             'a { color: #0000f5; text-decoration: none}'
                             'body { background-color: #f0f8fc; width:100%; }'
                             'p {font-family: courier new;}'
                             '</style>'
                             '</head><body><div>')
            self.log.warning('<div style="width:310px;">'
                        '<div style="background-color:#0066cc; text-align:center;width:150px; color:#e4e4e4; float:left;">Цвет каталогов</div>'
                        '<div style="background-color:#44cfa3; width:150px; color:#e4e4e4;text-align:center; float:right;">Цвет файлов</div>'
                        '<div style="background-color:#44cfa3; width:150px; color:#e4e4e4;text-align:center; float:right;"></div>'
                        '</div><br><hr>')
            self.log.warning('<div class="tab"><table class="res" border="1" cellpadding="0" cellspacing="0">')
            self.log.warning('<tr align="center" bgcolor="#999999"><td>Путь</td><td>Оригинальное название</td><td>Переименование</td></tr>')
            self.renamer(target)
            self.renamer_additional(target)
            self.log.warning('</table></div>')
            print ('Все файлы и каталоги в директории %s переименованы.\n' % target)
            html, js = self.get_files(target)
            print('Найденные *.html файлы.')
            for file in html:
                print (file)
            print('\n')
            print('Найденные *.js файлы.')
            for file in js:
                print (file)
            print('\n')
            self.parser(html, js)

            self.log.warning('</div></body></html>')
            Renamer()._exit()

    def renamer(self, dir):
        dirs = os.listdir(dir)
        for i in dirs:
            if os.path.isdir(dir+"\\"+i):
                self.renamer(dir+"\\"+i)
                if re.search('[а-яА-Я]', i):
                    try:
                        nw = transliterate.translit(i, 'ru', reversed=True)
                        if ' ' in nw:
                            nw = nw.replace(' ', '_')
                        os.rename(dir+'\\'+i, dir+'\\'+nw)
                        self.log.warning('<tr><td>%s</td><td bgcolor="#0066cc" class="text">%s</td><td bgcolor="#0066cc" class="text">%s</td></tr>' % (dir, i, nw))
                    except FileExistsError as err:
                        self.log.warning('<tr bgcolor="#ffa799"><td colspan="3"><div style="background-color:#0066cc; color:#e4e4e4; width:100px;">Каталог</div> %s</td></tr>' % (err))
                        print(err)
            elif re.search('[а-яА-Я]', i):
                try:
                    nw = transliterate.translit(i, 'ru', reversed=True)
                    if ' ' in nw:
                       nw = nw.replace(' ', '_')
                    #r = nw.rsplit('.', 1)
                    #nw = r[0]+'.'+r[1].lower()
                    nw = nw.replace('.PNG','.png')
                    nw = nw.replace('.JPG','.jpg')
                    os.rename(dir+'\\'+i, dir+'\\'+nw)
                    self.log.warning('<tr><td>%s</td><td bgcolor="#44cfa3">%s</td><td bgcolor="#44cfa3">%s</td></tr>' % (dir, i, nw))
                except FileExistsError as err:
                    self.log.warning('<tr bgcolor="#ffa799"><td colspan="3"><div style="background-color:#44cfa3; width:100px;">Файл</div>%s</td></tr>' % (err))
                    print(err)

    def renamer_additional(self, dir):
        # all other files
        dirs = os.listdir(dir)
        try:
            dirs.remove('res')
            print('deleted')
        except:
            print('nothing to delete')
        for i in dirs:
            if os.path.isdir(dir+"\\"+i) and not 'res' in i:
                    self.renamer(dir+"\\"+i)
                    try:
                        if ' ' in i:
                            nw = i.replace(' ', '_')
                            os.rename(dir+'\\'+i, dir+'\\'+nw)
                    except FileExistsError as err:
                        print(err)
            else:
                if not '_blah_log' in i:
                    try:
                        nw = i
                        if ' ' in i:
                           nw = i.replace(' ', '_')
                        #r = nw.rsplit('.', 1)
                        #nw = r[0]+'.'+r[1].lower()
                        nw = nw.replace('.PNG','.png')
                        nw = nw.replace('.JPG','.jpg')
                        os.rename(dir+'\\'+i, dir+'\\'+nw)
                    except FileExistsError as err:
                        print(err)
                else:
                    continue

    def get_files(self, target):
        html = list()
        js = list()
        tree = os.walk(target)
        for root, dirs, files in tree:
            if files:
                for file in files:
                    if not file.startswith('_blah_log'):
                        if file.endswith('.html'):
                            html.append(root+'\\'+file)
                        elif file.endswith('.js'):
                            js.append(root+'\\'+file)
        self.log.warning('<div class="tab2"><table class="res" border="1" cellpadding="0" cellspacing="0">')
        self.log.warning('<tr align="center" bgcolor="#999999"><td>Найденные .html файлы</td>></tr>')
        for file in html:
            self.log.warning('<tr><td><a href="%s">%s</a></td></tr>' % (file, file))
        for file in js:
            self.log.warning('<tr><td><a href="%s">%s</a></td></tr>' % (file, file))
        self.log.warning('</table></div>')
        return html, js

    def parser(self, html, js):
        self.log.warning('<div class="tab"><table class="res" border="1" cellpadding="0" cellspacing="0">')
        self.log.warning('<tr align="center" bgcolor="#999999"><td colspan="3">Что заменили в html файлах.</td>></tr>')
        for file in html:
            try:
                with open(file, encoding="utf-8") as f:
                    text = f.read()
            except:
                self.log.warning('<div><font color="#ff0000">Не открылась, плохая кодировка %s</font></div>' % file)
            #links = re.findall(r'(href|src)(\s=|=)(\s|)(\'|\").+?(\'|\")', text)
            links = re.findall(r'href[\s=|=][\'|\"].+?[\'|\"]|src[\s=|=][\'|\"].+?[\'|\"]', text)
            #links = filter(lambda x: re.search('[а-я]', x) and x , links)
            new_text = text
            print('В файле %s:' % (file))
            self.log.warning('<tr><td>%s</td><td>' % (file))
            for link in links:
                tlink = transliterate.translit(link, 'ru', reversed=True)
                tlink = tlink.replace(' ', '_')
                tlink = tlink.replace('.JPG','.jpg')
                tlink = tlink.replace('.PNG','.png')
                new_text = new_text.replace(link, tlink)
                print('%s -> %s' % (link, tlink))
                self.log.warning('<table class="res" border="1" cellpadding="1" cellspacing="1"><tr><td>%s</td><td>%s</td></tr></table>' % (link, tlink))
            self.log.warning('</td></tr>')
            print('\n')
            # links = re.findall(r'href[\s=|=][\'|\"].+?[\'|\"]|src[\s=|=][\'|\"].+?[\'|\"]', new_text)
            # for link in links:
            #     tlink = link.replace(' ', '_')
            #     tlink = tlink.replace('.JPG','.jpg')
            #     tlink = tlink.replace('.PNG','.png')
            #     new_text = text.replace(link, tlink)
            #     print('additional: %s -> %s' % (link, tlink))
            with open(file, 'w', encoding="utf-8") as f:
                f.write(new_text)
        self.log.warning('</table></div>')

        self.log.warning('<div class="tab"><table class="res" border="1" cellpadding="0" cellspacing="0">')
        self.log.warning('<tr align="center" bgcolor="#999999"><td colspan="3">Что заменили в js файлах.</td>></tr>')
        for file in js:
            try:
                with open(file, encoding="utf-8") as f:
                    text = f.read()
            except:
                self.log.warning('<div>Не открылась, плохая кодировка %s</div>' % file)
            #links = re.findall('link:[ {0,4}]\S+[\'|"]', text)
            links = re.findall('link:[\s|][\'|\"].+?[\'|\"]', text)
            #links = filter(lambda x: re.search('[а-я]', x) and x , links)
            new_text = text
            print('В файле %s:' % (file))
            self.log.warning('<tr><td>%s</td><td>' % (file))
            # Чтобы не ставил нижнее подчеркивание после link:_
            # убираем из ссылок link: и проходим по новому списку
            cut_links = list(map(lambda x: x.split('link:')[-1].strip(), links))
            #print('######################nhfnhfnhfnhf##################\n')
            #print(links)
            #print(cut_links)
            #print('######################nhfnhfnhfnhf##################\n')
            for link in cut_links:
                tlink = transliterate.translit(link, 'ru', reversed=True)
                tlink = tlink.replace(' ', '_')
                tlink = tlink.replace('.JPG','.jpg')
                tlink = tlink.replace('.PNG','.png')
                new_text = new_text.replace(link, tlink)
                print('%s -> %s' % (link, tlink))
                self.log.warning('<table class="res" border="1" cellpadding="1" cellspacing="1"><tr><td>%s</td><td>%s</td></tr></table>' % (link, tlink))
            self.log.warning('</td></tr>')
            print('\n')
            # links = re.findall('link:[\s|][\'|\"].+?[\'|\"]', new_text)
            # for link in links:
            #     tlink = link.replace(' ', '_')
            #     tlink = tlink.replace('.JPG','.jpg')
            #     tlink = tlink.replace('.PNG','.png')
            #     new_text = text.replace(link, tlink)
            #     print('additional: %s -> %s' % (link, tlink))
            with open(file, 'w', encoding="utf-8") as f:
                f.write(new_text)
        self.log.warning('</table></div>')


class Renamer:
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
        self.label = Label(root, text='Введите директории для обследования через запятую.').pack(expand=YES, fill=BOTH)

        self.txt = Text(root,width=150,height=10,font=('courier new',10), background='gray95', wrap=WORD)
        self.txt.pack(expand=YES,fill=BOTH)

        buttStart = ttk.Button(root, command=self._get_dir, text='Старт')
        buttStart.pack(side = 'left')

        cmenu = Menu(root, tearoff=False)
        cmenu.add_command(label="insert", command=self._paste)

    def _exit(self):
        root.destroy()
        sys.exit()

    def _help(self):
        help = Tk()
        txt = Text(help,width=75,height=20,background='gray95', font=('times',12),wrap=WORD)
        txt.pack(expand=YES,fill=BOTH)
        txt.insert(END, 'Программа рекурсивно переименовывает с русского в транслитерацию все каталоги и файлы \
    в каждой указанной директории.\n\n\
    Для правильной работы, в поле ввода текста, напишите все директории, которые нужно обследовать.\
    После чего нажмите кнопку "Старт". В каждой директории появится папка res в которой будет отдельный лог файл,\
    открывающийся в браузере.')
        #установка тегов для областей текста
        txt.tag_add('title','1.0','1.end')
        #конфигурирование тегов
        txt.tag_config('title', foreground='red', font=('times',14,'underline'),justify=CENTER)
        help.mainloop()

    def _get_dir(self):
        self.targets = list()
        tar = self.txt.get('1.0', 'end').split(',')
        for x in tar:
            if x:
                self.targets.append('%s' % x.replace('\n',''))
            else:
                continue
        Logic(self.targets)

    def _paste(self):
        try:
            self.txt.insert("current", root.clipboard_get())
        except tkinter.TclError:
            pass


root = Tk()
root.title("Renamer v.1.0")
# на весь экран
#root.wm_state('zoomed')
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 8
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.wm_geometry("+%d+%d" % (x, y))
obj_menu = Renamer()
root.mainloop()