# -*- coding: utf-8 -*-
__author__ = 'Dmitry Kryukov'
__email__ = "remasik@gmail.com"

import os
import re
import logging
import transliterate


####################################################################
targets = [r'C:\Users\PK-DPI-742\Desktop\web_resources12',
        ]

####################################################################
def renamer(dir):
    dirs = os.listdir(dir)
    for i in dirs:
        if os.path.isdir(dir+"\\"+i):
            renamer(dir+"\\"+i)
            if re.search('[а-яА-Я]', i):
                try:
                    nw = transliterate.translit(i, 'ru', reversed=True)
                    os.rename(dir+'\\'+i, dir+'\\'+nw)
                    log.warning('<tr><td>%s</td><td bgcolor="#0066cc" class="text">%s</td><td bgcolor="#0066cc" class="text">%s</td></tr>' % (dir, i, nw))
                except FileExistsError as err:
                    log.warning('<tr bgcolor="#ffa799"><td colspan="3"><div style="background-color:#0066cc; color:#e4e4e4; width:100px;">Каталог</div> %s</td></tr>' % (err))
                    print(err)
        elif re.search('[а-яА-Я]', i):
            try:
                nw = transliterate.translit(i, 'ru', reversed=True)
                os.rename(dir+'\\'+i, dir+'\\'+nw)
                log.warning('<tr><td>%s</td><td bgcolor="#44cfa3">%s</td><td bgcolor="#44cfa3">%s</td></tr>' % (dir, i, nw))
            except FileExistsError as err:
                log.warning('<tr bgcolor="#ffa799"><td colspan="3"><div style="background-color:#44cfa3; width:100px;">Файл</div>%s</td></tr>' % (err))
                print(err)

def get_files(target):
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
    log.warning('<div class="tab2"><table class="res" border="1" cellpadding="0" cellspacing="0">')
    log.warning('<tr align="center" bgcolor="#999999"><td>Найденные .html и .js файлы</td>></tr>')
    for file in html:
        log.warning('<tr><td><a href="%s">%s</a></td></tr>' % (file, file))
    for file in js:
        log.warning('<tr><td><a href="%s">%s</a></td></tr>' % (file, file))
    log.warning('</table></div>')
    return html, js

def parser(html, js):
    log.warning('<div class="tab"><table class="res" border="1" cellpadding="0" cellspacing="0">')
    log.warning('<tr align="center" bgcolor="#999999"><td colspan="3">Что заменили в html файлах.</td>></tr>')
    for file in html:
        try:
            with open(file, encoding="utf-8") as f:
                text = f.read()
        except:
            log.warning('<div>Не открылась, плохая кодировка %s</div>' % file)
        links = re.findall('src=\S+[\'|"]|href=\S+[\'|"]', text)
        links = filter(lambda x: re.search('[а-я]', x) and x , links)
        new_text = text
        print('В файле %s:' % (file))
        log.warning('<tr><td>%s</td><td>' % (file))
        for link in links:
            tlink = transliterate.translit(link, 'ru', reversed=True)
            new_text = new_text.replace(link, tlink)
            print('%s -> %s' % (link, tlink))
            log.warning('<table class="res" border="1" cellpadding="1" cellspacing="1"><tr><td>%s</td><td>%s</td></tr></table>' % (link, tlink))
        log.warning('</td></tr>')
        print('\n')
        with open(file, 'w', encoding="utf-8") as f:
            f.write(new_text)
    log.warning('</table></div>')

    log.warning('<div class="tab"><table class="res" border="1" cellpadding="0" cellspacing="0">')
    log.warning('<tr align="center" bgcolor="#999999"><td colspan="3">Что заменили в js файлах.</td>></tr>')
    for file in js:
        try:
            with open(file, encoding="utf-8") as f:
                text = f.read()
        except:
            log.warning('<div>Не открылась, плохая кодировка %s</div>' % file)
        links = re.findall('link:[ {0,4}]\S+[\'|"]', text)
        links = filter(lambda x: re.search('[а-я]', x) and x , links)
        new_text = text
        print('В файле %s:' % (file))
        log.warning('<tr><td>%s</td><td>' % (file))
        for link in links:
            tlink = transliterate.translit(link, 'ru', reversed=True)
            new_text = new_text.replace(link, tlink)
            print('%s -> %s' % (link, tlink))
            log.warning('<table class="res" border="1" cellpadding="1" cellspacing="1"><tr><td>%s</td><td>%s</td></tr></table>' % (link, tlink))
        log.warning('</td></tr>')
        print('\n')
        with open(file, 'w', encoding="utf-8") as f:
            f.write(new_text)
    log.warning('</table></div>')


if __name__ == '__main__':
    target_counter = 0
    # Проход по папкам
    for target in targets:
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
        log = logging.getLogger(target+'\\res\\'+str(target_counter))
        log.warning('<html><head>'
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
        log.warning('<div style="width:310px;">'
                    '<div style="background-color:#0066cc; text-align:center;width:150px; color:#e4e4e4; float:left;">Цвет каталогов</div>'
                    '<div style="background-color:#44cfa3; width:150px; color:#e4e4e4;text-align:center; float:right;">Цвет файлов</div>'
                    '<div style="background-color:#44cfa3; width:150px; color:#e4e4e4;text-align:center; float:right;"></div>'
                    '</div><br><hr>')
        log.warning('<div class="tab"><table class="res" border="1" cellpadding="0" cellspacing="0">')
        log.warning('<tr align="center" bgcolor="#999999"><td>Путь</td><td>Оригинальное название</td><td>Переименование</td></tr>')
        # Рекурсивное переименование
        renamer(target)
        log.warning('</table></div>')
        print ('Все файлы и каталоги в директории %s переименованы.\n' % target)
        # Поиск файлов
        html, js = get_files(target)
        print('Найденные *.html файлы.')
        for file in html:
            print (file)
        print('\n')
        print('Найденные *.js файлы.')
        for file in js:
            print (file)
        print('\n')
        # переименование ссылок в файлах
        parser(html, js)
        log.warning('</div></body></html>')