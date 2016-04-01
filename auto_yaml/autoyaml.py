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
import io


class Logic:
    def __init__(self, targets):
        self.targets = targets
        target_counter = 0

        targ = self.targets[0]
        tar = targ.rsplit('\\', 2)[0]
        f = io.open(tar+'\\auto_syllabus.yaml', 'wt', encoding="utf-8")
        f.write(u'topics:\n')
        f.close()

        # Проход по папкам
        for target in self.targets:
            target_counter += 1
            res = target+r'\YAML'
            lesson = target.rsplit('\\')[-2]
            if not os.path.exists(res):
                try:
                    os.mkdir(res)
                    print (u'>>> Папка YAML в  %s создана.' % target)
                except:
                    raise

            if os.path.exists(target+r'\YAML\_blah_log'+str(target_counter)+'.html'):
                try:
                    os.remove(target+r'\YAML\_blah_log'+str(target_counter)+'.html')
                except:
                    raise

            logger = logging.getLogger(target+'\\YAML\\'+str(target_counter))
            logger.addHandler(logging.FileHandler(target+'\\YAML\_blah_log'+str(target_counter)+'.html'))
            self.log = logging.getLogger(target+'\\YAML\\'+str(target_counter))
            self.log.warning('<html><head>'
                             '<meta charset="utf-8">'
                             '<style type="text/css">'
                             '.res{ width:100%; background-color: #eeeeee; border-width:1px; color: #232323; cellpadding: 5px; font-family: courier new; font-size: 12px;}'
                             '.tab{max-width:940px;}'
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

            self.log.warning('<div style="width:750px;">'
                            '<div style="background-color:#ff0000; text-align:center;width:350px; color:#232323; float:left;">Дублирование данных</div>'
                            '<div style="background-color:#999900; width:350px; color:#e4e4e4;text-align:center; float:right;">В файле один id, проверить является ли он ключом</div>'
                            '</div><br><hr>')
            dd = os.listdir(target)
            files = list()
            for x in dd:
                if x.endswith('.html'):
                    files.append(x)
            self.log.warning(u'<p><font color="blue">%s</font></p>' % ('#'*148))
            self.log.warning(u'<p>Обработка каталога: %s</p><hr>' % (target))
            self.log.warning('<div class="tab"><table class="res" border="1" cellpadding="0" cellspacing="0">')
            self.log.warning(u'<tr align="center" bgcolor="#999999"><td width="160px">Файл</td><td width="260px">OpenTask</td><td width="260px">Key Question</td><td width="260px">OpenQuizz</td></tr>')

            if 'index.html' in files:
                index = 'index.html'
            else:
                index = 'ffffffffffffffffffff'
            f = io.open(tar+'\\auto_syllabus.yaml', 'at', encoding="utf-8")
            f.write(u'\n')
            f.write(u' - name: iiiiiiiiiiiiiiiiiiiiiiiiiiii\n')
            f.write(u'   folder: %s\n' % lesson)
            f.write(u'   assignments:\n')
            f.write(u'   - imscc_identifier: iiiiiiiiiiiiiiiiiiiiiiiiiiii\n')
            f.write(u'     file_name: %s\n' % index)
            f.write(u'   lessons:\n')
            f.close()
            for file in files:
                with open(target+'\\'+file) as f:
                    file_text = f.read()
                opentask_dirty = re.findall(r'openTask\(event,.*\)', file_text)
                openquizz_dirty = re.findall(r'openQuizz\(event,.*\)', file_text)
                opentask = list()
                openquizz = list()
                key_opentask = 'iiiiiiiiiiiiiiiiiiiiiiiiiiii'
                dupl_key_opentask = ''
                dupl_opentask = list()

                if opentask_dirty:
                    for x in opentask_dirty:
                        c = x.split("'")[1]
                        opentask.append(c)

                if openquizz_dirty:
                    for x in openquizz_dirty:
                        c = x.split("'")[1]
                        openquizz.append(c)

                # Логирование
                if opentask and openquizz:
                    self.log.warning(u'<tr><td>%s</td>' % (file))
                    if len(opentask) > 1:
                        key_opentask = opentask.pop()
                        if key_opentask in opentask:
                            self.log.warning(u'<td bgcolor="#ff000">%s</td><td bgcolor="#ff000">%s</td>' % (opentask, key_opentask))
                            self.log.warning(u'<td>')
                            for x in openquizz:
                                self.log.warning(u'%s' % x)
                            self.log.warning(u'</td>')
                            dupl_opentask = opentask
                            dupl_key_opentask = key_opentask
                        else:
                            self.log.warning(u'<td>')
                            for x in opentask:
                                self.log.warning(u'%s <br>' % (x))
                            self.log.warning(u'</td>')
                            self.log.warning(u'<td>%s</td>' % key_opentask)
                            self.log.warning(u'<td>')
                            for x in openquizz:
                                self.log.warning(u'%s' % (x))
                            self.log.warning(u'</td>')
                    elif len(opentask) == 1:
                        self.log.warning(u'<td bgcolor="#999900">')
                        for x in opentask:
                            self.log.warning(u'%s' % (x))
                        self.log.warning(u'</td>')
                        self.log.warning(u'<td bgcolor="#999900">Проверить</td><td>none</td>')
                        self.log.warning(u'<td>')
                        for x in openquizz:
                            self.log.warning(u'%s' % (x))
                        self.log.warning(u'</td>')
                    self.log.warning(u'</tr>')
                elif opentask and not openquizz:
                    self.log.warning(u'<tr><td>%s</td>' % (file))
                    if len(opentask) > 1:
                        key_opentask = opentask.pop()
                        if key_opentask in opentask:
                            self.log.warning(u'<td bgcolor="#ff000">%s</td><td bgcolor="#ff000">%s</td><td>none</td>' % (opentask, key_opentask))
                            dupl_opentask = opentask
                            dupl_key_opentask = key_opentask
                        else:
                            self.log.warning(u'<td>')
                            for x in opentask:
                                self.log.warning(u'%s' % (x))
                            self.log.warning(u'</td>')
                            self.log.warning(u'<td>%s</td><td>none</td>' % key_opentask)

                    elif len(opentask) == 1:
                        self.log.warning(u'<td bgcolor="#999900">')
                        for x in opentask:
                            self.log.warning(u'%s' % (x))
                        self.log.warning(u'</td>')
                        self.log.warning(u'<td bgcolor="#999900">Проверить</td><td>none</td>')
                    self.log.warning(u'</tr>')

                elif not opentask and openquizz:
                    self.log.warning(u'<tr><td>%s</td><td>none</td><td>none</td></tr>' % file)
                    self.log.warning(u'<td>')
                    for x in openquizz:
                        self.log.warning(u'%s' % x)
                    self.log.warning(u'</td>')
                else:
                    self.log.warning(u'<tr bgcolor="#dbdbdb"><td>%s</td><td>none</td><td>none</td><td>none</td></tr>' % file)

                # Продолжение работы программы
                print file
                print lesson
                print 'opentask', opentask
                print 'key', key_opentask
                print 'quizz', openquizz
                print '\n'*3

                f = io.open(tar+'\\auto_syllabus.yaml', 'at', encoding="utf-8")
                if 'index' in file:
                    if index != file:
                        f.write(u'   - name: iiiiiiiiiiiiiiiiiiiiiiiiiiii\n')
                        f.write(u'     pages:\n')
                        f.write(u'     - file_name: %s\n' % file)
                        f.write(u'     key_questions:\n')
                        if dupl_key_opentask:
                            f.write(u'     - imscc_identifier: %s\n' % 'iiiiiiiiiiiiiiiiiiiiiiiiiiii')
                        else:
                            f.write(u'     - imscc_identifier: %s\n' % key_opentask)
                        f.write(u'     assignments:\n')
                        if opentask:
                            for x in opentask:
                                f.write(u'     - imscc_identifier: %s\n' % x)
                                f.write(u'       required_by_default: true\n')
                                f.write(u'       mark_can_be_given: true\n')
                        else:
                            for x in range(10):
                                f.write(u'     - imscc_identifier: iiiiiiiiiiiiiiiiiiiiiiiiiiii \n')
                                f.write(u'       required_by_default: true\n')
                                f.write(u'       mark_can_be_given: true\n')
                        f.write(u'     quizzes:\n')
                        if openquizz:
                            for x in openquizz:
                                f.write(u'     - imscc_identifier: %s\n' % x)
                        else:
                            f.write(u'     - imscc_identifier: iiiiiiiiiiiiiiiiiiiiiiiiiiii\n')
                f.close()
            self.log.warning('</table></div>')
            self.log.warning('</div></body></html>')
        Autoyaml()._exit()



class Autoyaml:
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
        self.label = Label(root, text='Введите директории занятий для обследования через запятую. Не ставьте в конце \ ').pack(expand=YES, fill=BOTH)

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
        txt.insert(END, 'Программа автоматического составления yaml файла ')
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
        Logic(self.targets)

    def _paste(self):
        try:
            self.txt.insert("current", root.clipboard_get())
        except tkinter.TclError:
            pass

root = Tk()
root.title("AutoYaml v.1.0")
# на весь экран
#root.wm_state('zoomed')
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 8
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.wm_geometry("+%d+%d" % (x, y))
obj_menu = Autoyaml()
root.mainloop()