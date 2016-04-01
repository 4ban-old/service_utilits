# coding: utf-8
__author__ = 'Dmitry Kryukov'
__email__ = "remasik@gmail.com"

from Tkinter import *
from tkFileDialog import *
import ttk
import sys
import re
import os
import logging
import shutil


class Logic:
    def __init__(self, targets, lessons):
        self.targets = targets
        self.lessons = lessons
        target_counter = 0
        # Проход по папкам
        for target in self.targets:
            target_counter += 1
            res = target+r'\COPIED_FILES'
            if not os.path.exists(res):
                try:
                    os.mkdir(res)
                    print (u'>>> Папка COPIED_FILES в  %s создана.' % target)
                except:
                    raise

            if os.path.exists(target+r'\COPIED_FILES\_blah_log'+str(target_counter)+'.html'):
                try:
                    os.remove(target+r'\COPIED_FILES\_blah_log'+str(target_counter)+'.html')
                except:
                    raise

            logger = logging.getLogger(target+'\\COPIED_FILES\\'+str(target_counter))
            logger.addHandler(logging.FileHandler(target+'\\COPIED_FILES\_blah_log'+str(target_counter)+'.html'))
            self.log = logging.getLogger(target+'\\COPIED_FILES\\'+str(target_counter))
            self.log.warning('<html><head>'
                             '<meta charset="utf-8">'
                             '<style type="text/css">'
                             '.res{ width:100%; background-color: #eeeeee; border-width:1px; color: #232323; cellpadding: 5px; font-family: courier new; font-size: 12px;}'
                             '.tab{max-width:100%;}'
                             '.tab2{max-width:50%;}'
                             '.text{color:#e4e4e4;}'
                             'a { color: #0000f5; text-decoration: none}'
                             'body { background-color: #f0f8fc; width:100%; }'
                             'p {font-family: courier new;}'
                             '.floates{width:100%; float:right; padding: 0px 10px 30px 0px;}'
                             '.spoiler_desc {background: #232323; color:#e4e4e4 ;padding: 0 5px;border-radius: 0 0 5px 5px;margin-top: 22px;}'
                             '.spoiler_desc p {cursor: text;color: #FFFFFF;}'
                             '.spoiler_close {display: none;width: 100%;height: 22px;background: #232323; color:#e4e4e4;border-radius: 5px 5px 0 0;text-indent: 10px;cursor: default;border-bottom: 1px dotted #000000;position: absolute;top: 0px;left: 0;}'
                             '.spoiler_close:hover { background: #313131; }'
                             '.spoiler_open:before {content: "Открыть";border-bottom: 0px dotted #000000;cursor: default;text-indent: 10px;border-radius: 5px 5px 0 0;width: 100%;height: 22px;background: #232323; color:#e4e4e4;display: block;position: absolute;top: 0px;left: 0;}'
                             '.spoiler_open:hover:before { background: #313131; }'
                             '.spoiler_open {margin: 5px 0 0 15px;height: 23px;width: 40%;outline: none;float: left;position: relative;overflow: hidden;-webkit-transition: height 0.3s ease;-moz-transition: height 0.3s ease;-ms-transition: height 0.3s ease;-o-transition: height 0.3s ease;transition: height 0.3s ease;}'
                             '.spoiler_open:focus { height: auto; width:40% }'
                             '.spoiler_open:focus .spoiler_close { display: block; }'
                             '.spoiler_open:focus:before { display: none; }'
                             '</style>'
                             '</head><body><div>')
            self.log.warning('<div style="width:310px;">'
                        '<div style="background-color:#0066cc; text-align:center;width:150px; color:#e4e4e4; float:left;">Цвет каталогов</div>'
                        '<div style="background-color:#44cfa3; width:150px; color:#e4e4e4;text-align:center; float:right;">Цвет файлов</div>'
                        '<div style="background-color:#44cfa3; width:150px; color:#e4e4e4;text-align:center; float:right;"></div>'
                        '</div><br><hr>')

            clean_id = self._get_id_yaml(target)
            dirs, files, assessments_files = self._finder(target)
            self._mover(clean_id, dirs, files, target)
            self._assessments_mover(clean_id, assessments_files, target)
            self._wiki_content_mover(self.lessons, target)
            self.log.warning('</div></body></html>')
            print 'finished'
            Finder()._exit()

    def _get_id_yaml(self, target):
        self.yaml = target+r'\web_resources\syllabus.yaml'
        self.target = target
        if os.path.exists(self.yaml):
            status = '<font color="#44cfa3">[OK]</font>'
        else:
            status = '<font color="#ff0000">[FAIL]</font>'
        self.log.warning(u'<div>Директория: %s</div>' % self.target)
        self.log.warning(u'<div>Путь к YAML: %s -  %s</div><hr>' % (self.yaml, status))
        self.log.warning(u'<div>Все айдишники в YAML файле.</div>')
        self.log.warning('<div class="floates"><div class="spoiler_open" tabindex="2"><div class="spoiler_desc">')
        self.log.warning('<div class="tab"><table class="res" border="1" cellpadding="0" cellspacing="0">')
        self.log.warning(u'<tr align="center" bgcolor="#999999"><td colspan="2">ID в YAML</td></tr>')
        clean_id = list()
        try:
            with open(self.yaml) as f:
                    all_yaml = f.read()
        except:
            print 'Nothing YAML to opening'
        else:
            dirty_id = re.findall('imscc_identifier: \S+', all_yaml)
            for i, x in enumerate(dirty_id):
                id = x.split()[-1]
                id = id.replace('"', '')
                clean_id.append(id)
                self.log.warning('<tr><td>%s</td><td>%s</td></tr>' % (i, id))
        self.log.warning('</table></div>')
        self.log.warning('</div><span tabindex="0" class="spoiler_close">Закрыть</span></div></div>')
        return clean_id

    def _finder(self, target):
        dirty_dirs = os.listdir(target)
        try:
            assessments_files = os.listdir(target+r'\non_cc_assessments')
        except:
            assessments_files = list()
        dirs = list()
        files = list()
        odd = list()
        for x in dirty_dirs:
            if os.path.isdir(target+x):
                # Костыль, вдруг айдишник будет короткий
                if len(x) > 20:
                    dirs.append(x)
                else:
                    odd.append(x)
            elif os.path.isfile(target+x):
                if x.endswith('xml'):
                    # Костыль, вдруг айдишник будет короткий
                    if len(x) > 17:
                        files.append(x)
                    else:
                        odd.append(x)
                else:
                    odd.append(x)
            else:
                self.log.warning('Что-то непонятное: %s' % target+x)
                continue
        # logging our result
        self.log.warning(u'<div>Все Файлы и каталоги в директории.</div>')
        self.log.warning('<div class="floates"><div class="spoiler_open" tabindex="2"><div class="spoiler_desc">')
        self.log.warning('<div class="tab"><table class="res" border="1" cellpadding="0" cellspacing="0">')
        self.log.warning(u'<tr align="center" bgcolor="#999999"><td colspan="1">Все файлы и каталоги</td></tr>')
        for x in dirty_dirs:
            self.log.warning('<tr><td>%s</td></tr>' % (x))
        self.log.warning('</table></div>')
        self.log.warning('</div><span tabindex="0" class="spoiler_close">Закрыть</span></div></div>')

        self.log.warning(u'<div>Файлы из non_cc_assessments.</div>')
        self.log.warning('<div class="floates"><div class="spoiler_open" tabindex="2"><div class="spoiler_desc">')
        self.log.warning('<div class="tab"><table class="res" border="1" cellpadding="0" cellspacing="0">')
        self.log.warning(u'<tr align="center" bgcolor="#999999"><td colspan="1">Исключенные файлы и каталоги</td></tr>')
        for x in assessments_files:
            self.log.warning('<tr><td>%s</td></tr>' % (x))
        self.log.warning('</table></div>')
        self.log.warning('</div><span tabindex="0" class="spoiler_close">Закрыть</span></div></div>')

        self.log.warning(u'<div>Исключенные файлы и каталоги.</div>')
        self.log.warning('<div class="floates"><div class="spoiler_open" tabindex="2"><div class="spoiler_desc">')
        self.log.warning('<div class="tab"><table class="res" border="1" cellpadding="0" cellspacing="0">')
        self.log.warning(u'<tr align="center" bgcolor="#999999"><td colspan="1">Исключенные файлы и каталоги</td></tr>')
        for x in odd:
            self.log.warning('<tr><td>%s</td></tr>' % (x))
        self.log.warning('</table></div>')
        self.log.warning('</div><span tabindex="0" class="spoiler_close">Закрыть</span></div></div>')

        self.log.warning(u'<div>Искомые файлы и папки.</div>')
        self.log.warning('<div class="floates"><div class="spoiler_open" tabindex="2"><div class="spoiler_desc">')
        self.log.warning('<div class="tab"><table class="res" border="1" cellpadding="0" cellspacing="0">')
        self.log.warning(u'<tr align="center" bgcolor="#999999"><td colspan="1">Исключенные файлы и каталоги</td></tr>')
        for x in dirs:
            self.log.warning('<tr bgcolor="#0066cc"><td><font color="#e4e4e4">%s</font></td></tr>' % (x))
        for x in files:
            self.log.warning('<tr bgcolor="#44cfa3"><td>%s</td></tr>' % (x))
        self.log.warning('</table></div>')
        self.log.warning('</div><span tabindex="0" class="spoiler_close">Закрыть</span></div></div>')
        return dirs, files, assessments_files

    def _mover(self, clean_id, dirs, files, target):
        for id in clean_id:
            if id in dirs:
                shutil.copytree(target+id, target+'\COPIED_FILES\\'+id)
        for id in clean_id:
            if id+'.xml' in files:
                shutil.copy(target+id+'.xml', target+'\COPIED_FILES\\'+id+'.xml')

    def _assessments_mover(self, clean_id, assessments_files, target):
        if not os.path.exists(target+'\COPIED_FILES\non_cc_assessments'):
            try:
                os.mkdir(target+r'\COPIED_FILES\non_cc_assessments')
                print (u'>>> Папка non_cc_assessments в  %s создана.' % target)
            except:
                raise
        for id in clean_id:
            if id+'.xml.qti' in assessments_files:
                shutil.copy(target+r'\non_cc_assessments\\'+id+r'.xml.qti', target+r'\COPIED_FILES\non_cc_assessments\\'+id+'.xml.qti')

    def _wiki_content_mover(self, lessons, target):
        html = list()
        for lesson in lessons:
            all = os.listdir(lesson)
            for x in all:
                if os.path.isfile(lesson+'\\'+x):
                    if x.endswith('.html'):
                        html.append(lesson+'\\'+x)
        print u'Собрал все .html файлы: %s' % len(html)
        forcopy = list()
        self.log.warning('<div class="tab"><table class="res" border="1" cellpadding="0" cellspacing="0">')
        self.log.warning(u'<tr align="center" bgcolor="#999999"><td>html</td><td>Ссылки</td></tr>')
        for x in html:
            print u'%s' % x
            self.log.warning(u'<tr><td>%s</td>' % x)
            with open(x) as f:
                txt = f.read()
            dirty_links = re.findall(r'../../wiki_content/.+?[\'|\"]', txt)
            clean_links = map(lambda x: x.replace('\'',''), dirty_links)
            links = map(lambda x: x.replace('../../wiki_content/',target+'\\wiki_content\\'), clean_links)
            print links
            forcopy+=links
            self.log.warning(u'<td>')
            for x in links:
                self.log.warning(u'%s<br>' % x)
            self.log.warning(u'</td></tr>')
        self.log.warning('</table></div>')
        self.log.warning('<div class="tab"><table class="res" border="1" cellpadding="0" cellspacing="0">')
        self.log.warning(u'<tr align="center" bgcolor="#999999"><td>Файлы</td><td>Статус</td></tr>')
        forcopy = list(set(forcopy))
        print forcopy
        if not os.path.exists(target+'\COPIED_FILES\wiki_content'):
            try:
                os.mkdir(target+r'\COPIED_FILES\wiki_content')
                print (u'>>> Папка wiki_content в  %s создана.' % target)
            except:
                raise
        for file in forcopy:
            try:
                shutil.copy(file, target+r'\COPIED_FILES\wiki_content\\')
            except:
                print u'Не смог скопировать %s' % file
                self.log.warning(u'<tr><td>%s</td><td bgcolor="#ff0000">Не скопирован></td></tr>' % file)
            else:
                print u'Файл %s скопирован' % file
                self.log.warning(u'<tr><td>%s</td><td bgcolor="#00ff00">Скопирован</td></tr>' % file)
        self.log.warning('</table></div>')
        print u'Файлы скопированы'

#self.log.warning(u'<tr><td></td><td></td><td></td></tr>')

class Finder:
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
        self.label = Label(root, text='Введите путь к курсу. Не ставьте в конце \ ').pack(expand=YES, fill=BOTH)

        self.txt = Text(root,width=100,height=3,font=('courier new',10), background='gray95', wrap=WORD)
        self.txt.pack(expand=YES,fill=BOTH)

        self.label2 = Label(root, text='Введите пути к занятиям через запятую. Не ставьте в конце \ ').pack(expand=YES, fill=BOTH)
        self.txt2 = Text(root,width=100,height=3,font=('courier new',10), background='gray95', wrap=WORD)
        self.txt2.pack(expand=YES,fill=BOTH)

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
        txt.insert(END, 'Программа для копирования всех директорий и файлов с id в имени из yaml файлов ')
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
                if x.endswith('\\'):
                    self.targets.append('%s' % x.replace('\n',''))
                else:
                    n= x.replace('\n','')
                    self.targets.append('%s' % n+'\\')
            else:
                continue

        self.lessons = list()
        tar2 = self.txt2.get('1.0', 'end').split(',')
        for x in tar2:
            if x:
                if x.endswith('\\'):
                    self.lessons.append('%s' % x.replace('\n',''))
                else:
                    n= x.replace('\n','')
                    self.lessons.append('%s' % n+'\\')
            else:
                continue
        Logic(self.targets, self.lessons)

    def _paste(self):
        try:
            self.txt.insert("current", root.clipboard_get())
        except tkinter.TclError:
            pass

root = Tk()
root.title("ID finder v.1.0")
# на весь экран
#root.wm_state('zoomed')
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 8
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.wm_geometry("+%d+%d" % (x, y))
obj_menu = Finder()
root.mainloop()