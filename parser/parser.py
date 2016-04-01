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
    Module
"""


import re
import requests
import lxml.html
import lxml.etree
import os
import logging

###################################################################
########################## Настройки ##############################
# Показывать приветствие?
show = False
# Страницы с курсами
# Если добавились новые курсы, рекомендуется перекачать страницы
# Так же нужно перекачивать эти фалйы для обработки новых курсов.
quizzes = 'C:\Users\PK-DPI-742\Desktop\q.html'
discussions = 'C:\Users\PK-DPI-742\Desktop\d.html'
# Шаблон поиска, что ищем
template = '54.72.205.30'
# Список папок для обхода
folders = [r'C:\Users\PK-DPI-742\Desktop\export\okr_mir_3\web_resources\3',
           #r'C:\Users\PK-DPI-742\Desktop\export\lit_chten_3\web_resources\4',
           #r'C:\Users\PK-DPI-742\Desktop\export\lit_chten_3\web_resources\5',
           #r'C:\Users\PK-DPI-742\Desktop\4',
           ]
###################################################################


def get_links(page, template, log, html_log):
    """
        Ищем все ссылки по шаблону
    :param page: ссылка на страницу в которой ищем
    :param template: шаблон по которому ищем
    :return:
    """
    # Парсим страницу в которой ищем
    page = lxml.html.parse(page)
    links = list()
    # Список для ссылок специальных, trener.html, пятого типа
    special = list()
    # Находим все ссылки
    all_links = page.xpath('//@href')
    for link in all_links:
        # Если шаблон присутствует в ссылке, сохраняем в список, остальные игнорируем
        if template in link:
            links.append(link)
        if '.html' in link and not template in link:
            special.append(link)
    if links:
        print u">>> Нашел %s ссылок по шаблону!" % len(links)
        #log.warning(u">>> Нашел %s ссылок по шаблону!" % len(links))
        html_log.warning(u"<p style='color:#50c878;'>Нашел %s ссылок по шаблону!</p>" % len(links))
        if special:
             print u">>> Также %s ссылок типа ***.html!" % len(special)
             #log.warning(u">>> Также %s ссылок типа ***.html!" % len(special))
             html_log.warning(u"<p style='color:#50c878;'>Также %s ссылок типа ***.html!</p>" % len(special))
        return links, special
    else:
        print u">>> Не нашел ни одной ссылки по шаблону!"
        #log.warning(u">>> Не нашел ни одной ссылки по шаблону!")
        html_log.warning(u'<p style="color:#ff0000;">Не нашел ни одной ссылки по шаблону!</p>')
        if special:
             print u">>> Но нашел %s ссылок типа ***.html!" % len(special)
             #log.warning(u">>> Но нашел %s ссылок типа ***.html!" % len(special))
             html_log.warning(u"<p style='color:#50c878;'>Но нашел %s ссылок типа ***.html!</p>" % len(special))
        return links, special


def get_courses(quizzes, discussions):
    try:
        courses_quiz = lxml.html.parse(quizzes)
    except:
        print u'Не могу распарсить quizzes.'
    else:
        print u'quizzes - %s распарсена.' % quizzes
    try:
        courses_discuss = lxml.html.parse(discussions)
    except:
        print u'Не могу распарсить discussions.'
    else:
        print u'discussions - %s распарсена.' % discussions
    return courses_quiz, courses_discuss


def downloader(links, link_text, log, template, html_log):
    """
        Логинится, переходит по ссылке, скачивает страничку, вытаскивает из нее текст по xpath
        в зависимости от типа страницы quizz, discussion, file, page.
    :param links: Все ссылки
    :param link_text: пустой словарь результатов функции
    :return: возвращает заполненный словарь
    """
    session = requests.Session()
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    # Логин и пароль к сайту, нужен для авторизованных страниц
    session.auth = ('osokin@mob-edu.ru', 'qwerty')
    session.headers.update({'x-test': 'true'})
    counter = 0
    html_log.warning('<table class="res" border="1" cellpadding="4" cellspacing="1">')
    html_log.warning(u'<tr><td colspan="3" align="center">Ход работы: ссылка - текст вытащенный из страницы (дубликаты показываются)</td></tr>')
    for link in links:
        counter += 1
        if template not in link:
            link_text.update({link : link})
            print u'[%s/%s]- обработана (спец.) %s - %s' % (counter, len(links), link, link)
            #log.warning(u'[%s/%s] %s - %s' % (counter, len(links), link, link))
            html_log.warning(u'<tr><td>[%s/%s]</td><td><a href="%s" target="_blank">%s</a></td><td>%s</td></tr>' % (counter, len(links), link, link, link))
        else:
            resp = session.get(link, headers={'x-test2': 'true'})
            resp.encoding = 'utf-8'
            resp = lxml.html.document_fromstring(resp.text)
            # Параметры для поиска title страницы в зависимости от типа страницы
            quiz = '//h1[@id="quiz_title"]/text()'
            discuss = '//h1[@class="discussion-title"]/text()'
            #page = '//span[@class="ellipsible"][last()]/text()' # Не пригодилось
            file = '//span[@class="ellipsible"][last()]/text()'
            find = list()
            if not find:
                find = resp.xpath(quiz)
            if not find:
                find = resp.xpath(discuss)
            if not find:
                if '/pages/' in link:
                    #find = resp.xpath(page) # Не пригодилось
                    find.append(link.split('/')[-1])
                if '/files/' in link:
                    find = resp.xpath(file)
                    find = [x.split('/')[-1] for x in find]
                    # Костыль
                    if '.html' not in find[0]:
                        find = ['###############']

            if not find:
                print u">>> На этой ссылке: %s ничего не нашел!" % link
                #log.warning(u"\n>>> На этой ссылке: %s ничего не нашел!" % link)
                html_log.warning(u"<p style='color:#ff0000;'>На этой ссылке: <a href='%s' target='_blank'>%s</a> ничего не нашел!</p>" % (link, link))
            else:
                if len(find) > 1:
                    # Сообщение выводится если по ссылке он найдет больше одного:
                    # title, навигационных блоков или у ссылки непредвиденное название
                    print u'>>> НА ЭТОЙ ССЫЛКЕ %s БОЛЬШЕ ОДНОГО РЕЗУЛЬТАТА!' % link
                    #log.warning(u'\n>>> НА ЭТОЙ ССЫЛКЕ %s БОЛЬШЕ ОДНОГО РЕЗУЛЬТАТА!' % link)
                    html_log.warning(u'<p style="color:#ff0000;">НА ЭТОЙ ССЫЛКЕ <a href="%s" target="_blank">%s</a> БОЛЬШЕ ОДНОГО РЕЗУЛЬТАТА!</p>' % (link, link))
                else:
                    find = find[0].strip()
                    link_text.update({link : find})
                    #print u"Ссылка %s/%s обработана. [%s - '%s']" % (counter, len(links), link, find)
                    print u'[%s/%s]- обработана %s - %s' % (counter, len(links), link, find)
                    #log.warning(u'[%s/%s] %s - %s' % (counter, len(links), link, find))
                    html_log.warning(u'<tr><td>[%s/%s]</td><td><a href="%s" target="_blank">%s</a></td><td>%s</td></tr>' % (counter, len(links), link, link, find))
    html_log.warning('</table>')
    print '\n'
    #log.warning('\n')
    return link_text


def get_ident(link_text, courses_quiz, courses_discuss, log, html_log):
    """
        Ищем найденные title на страницах с курсами, получаем их идентификаторы
    :param link_text: словарь вида: ссылка - текст
    :return: словарь вида: ссылка - идентификатор
    """
    result = dict()
    double_result = dict()
    not_found = dict()
    for link, text in link_text.items():
        resp = list()
        if '/quizzes/' in link:
            text = text.replace("'",'"')
            p = u'//a[@class="ng-binding"][contains(., \''
            p += text
            p += u'\')]/@href'
            resp = courses_quiz.xpath(p)
        elif '/discussion_topics/' in link:
            text = text.replace("'",'"')
            p = u'//a[@class="ng-binding"][contains(., \''
            p += text
            p += u'\')]/@href'
            resp = courses_discuss.xpath(p)
        elif '/pages/' in link:
            resp = [text]
        elif '/files/' in link:
            resp = [text]
        else:
            resp = [text]

        if not resp:
            not_found.update({link : text})
            print u'>>> Ничего не нашел: %s \n %s \n %s' % (link, text, resp)
            print '#'*50
            #log.warning( u'\n>>> Ничего не нашел: %s \n %s \n %s' % (link, text, resp))
            #log.warning('#'*50)
            html_log.warning(u'<p style="color:#ff0000;">Ничего не нашел: %s <br> %s <br> %s</p>' % (link, text, resp))
        elif len(resp) > 1:
            print u'>>> БОЛЬШЕ ОДНОГО СОВПАДЕНИЯ В НОВОЙ СИСТЕМЕ: %s - %s' % (link, text)
            #log.warning(u'\n>>> БОЛЬШЕ ОДНОГО СОВПАДЕНИЯ В НОВОЙ СИСТЕМЕ: %s - %s' % (link, text))
            html_log.warning(u'<p style="color:#ff0000;">БОЛЬШЕ ОДНОГО СОВПАДЕНИЯ В НОВОЙ СИСТЕМЕ: <br><a href="%s">%s</a> - %s</p>' % (link, link, text))
            for res in resp:
                print res
                #log.warning(res)
                html_log.warning('<p><a href="%s">%s</a></p>' % (res, res))
            print '#'*50
            #log.warning('#'*50)
            double_result.update({link : resp})
            # Возможно стоит сделать добвления всех совпадений в result
            # и заменять в файле ссылку несколько раз, на resp[0], resp[1], resp[2] и тд.
        else:
            # режет ссылки вида css/trener.html
            resp = resp[0].split('/')[-1]
            result.update({link : resp})
    return result, double_result, not_found


def replacer(copy, result, new_file, link_text, double_result, not_found, log, html_log):
    # Заменяем ссылки в тексте
    for link, text in result.items():
        if link in copy:
            if '###############' in text:
                print u'%s - Не существует!' % link
                #log.warning(u'%s - Не существует!.' % link)
                html_log.warning(u'<p style="color:#ff0000;"><a href="%s">%s</a> - не существует!.</p>' % (link, link))
                continue
            if '/pages/' in link:
                new = '#'
                new += '" onclick="LmsProxy.getInstance().showWiki(event, \'../../wiki_content/'+text
                new += '.html\')'
                copy = copy.replace(link, new)
            if '/files/' in link:
                new = '#'
                new += '" onclick="LmsProxy.getInstance().showResource(event, \''+text
                new += '\')'
                copy = copy.replace(link, new)
            if '/quizzes/' in link:
                new = '#'
                new += '" onclick="LmsProxy.getInstance().openQuizz(event, \''+text
                new += '\')'
                copy = copy.replace(link, new)
            if '/discussion_topics' in link:
                new = '#'
                new += '" onclick="LmsProxy.getInstance().openTask(event, \''+text
                new += '\')'
                copy = copy.replace(link, new)
            # для ссылок пятого типа
            #if 'href="'+link+'"' in copy:
            if link == text:
                new = '#'
                new += '" onclick="LmsProxy.getInstance().showResource(event, \''+text
                new += '\')'
                copy = copy.replace(link, new)
            # Изменение происходило после проверок, но тогда плохо сработало бы первое условие
            # могло заменить ссылку вида href="css/trener.html" на ''
            # Поэтому сделал замену отдеьно после каждой проверки.
            #copy = copy.replace(link, new)
            # Удаление ненужного
            copy = copy.replace('<base target="_blank"/>', '')
            copy = copy.replace('<base target="_blank">', '')
            if '<script src="../js/lms_proxy.js" type="text/javascript"></script>' not in copy:
                copy = copy.replace('</head>', '<script src="../js/lms_proxy.js" type="text/javascript"></script>\n  </head>')

    # сохраняем в новый файл замененные ссылки
    try:
        with open(new_file, 'w') as f:
            f.write(copy)
        print u'>>> Файл %s записан успешно.' % new_file
        #log.warning(u'>>> Файл %s записан успешно.' % new_file)
        html_log.warning(u'<p>Файл %s записан успешно.</p>' % new_file)
    except:
        print u'>>> Не получилось записать результат в файл - %s' % new_file
        #log.warning(u'>>> Не получилось записать результат в файл - %s' % new_file)
        html_log.warning(u'<p style="color:#ff0000;">Не получилось записать результат в файл - %s</p>' % new_file)
    else:
        print u'>>> Заменены %s/%s ссылок (Ссылки-дубликаты не учитывались)' % (len(result), len(link_text))
        #log.warning(u'>>> Заменены %s/%s ссылок (Ссылки-дубликаты не учитывались)' % (len(result), len(link_text)))
        html_log.warning(u'<p>Заменены %s/%s ссылок (Ссылки-дубликаты не учитывались)</p>' % (len(result), len(link_text)))
        if double_result:
            print u'>>> НАЙДЕНЫ ДУБЛИКАТЫ!!!!!:'
            #log.warning(u'>>> НАЙДЕНЫ ДУБЛИКАТЫ!!!!!:')
            html_log.warning(u'<p style="color:#ff0000;">НАЙДЕНЫ ДУБЛИКАТЫ!!!!!:</p>')
            for link, text in double_result.items():
                print link
                #log.warning(link)
                html_log.warning(u'<p><a href="%s">%s</a></p>' % (link, link))
        if not_found:
            print '#'*50
            print u'>>> Не найдены совпадения для следующих ссылок:'
            #log.warning('#'*50)
            #log.warning(u'>>> Не найдены совпадения для следующих ссылок:')
            html_log.warning(u'<p>Не найдены совпадения для следующих ссылок (Попробуйте поискать вручную):</p>')
            for link, text in not_found.items():
                text = text.replace('"', "'")
                print u"%s - %s" % (link, text)
                #log.warning(u"%s - $s" % (link, text))
                html_log.warning(u'<p><a href="%s">%s</a> - %s</p>' % (link, link, text))
            print '#'*50
            #log.warning('#'*50)


if __name__ == '__main__':
    if show:
        with open('ascii') as f:
            ascii = f.read()
        print ascii
    print '\n'
    print "#"*50
    print u"Шаблон поиска: %s" % template
    # Парсим страницы с курсами
    courses_quiz, courses_discuss = get_courses(quizzes, discussions)
    print "#"*50
    print "#"*50
    print "#"*50

    folder_counter = 0
    for folder in folders:
        # Папка для сохранения результата
        new_folder = folder+r'\res'
        # Проверим наличие каталога res, если его нет создадим.
        if not os.path.exists(new_folder):
            try:
                os.mkdir(new_folder)
                print u'>>> Папка res создана.'
            except:
                raise
        # Логирование
        #logname = folder.split('\\')[-1]
        #if os.path.exists(folder+r'\res\\'+logname+'.txt'):
        #    try:
        #        os.remove(folder+r'\res\\'+logname+'.txt')
        #    except:
        #        raise
        #logger = logging.getLogger(folder+r'\res\\'+logname)
        #logger.addHandler(logging.FileHandler(folder+r'\res\\'+logname+'.txt'))
        #log = logging.getLogger(folder+r'\res\\'+logname)
        log = 'empty'
        # Логирование в html
        htmllog = folder.split('\\')[-1]+'_log'
        if os.path.exists(folder+r'\res\\'+htmllog+'.html'):
            try:
                os.remove(folder+r'\res\\'+htmllog+'.html')
            except:
                raise
        html_logger = logging.getLogger(folder+r'\res\\'+htmllog)
        html_logger.addHandler(logging.FileHandler(folder+r'\res\\'+htmllog+'.html'))
        html_log = logging.getLogger(folder+r'\res\\'+htmllog)
        html_log.warning('<html>\n<head>\n'
                         '<meta charset="utf-8">'
                         '<style type="text/css">\n'
                         '.res{ background-color: #eeeeee; border-width:1px; color: #232323; cellpadding: 5px; font-family: courier new;}\n'
                         'a { color: #0000f5; text-decoration: none}\n'
                         'body { background-color: #f0f8fc; }\n'
                         'p {font-family: courier new;}'
                         '\n</style>'
                         '</head>\n<body>\n<div>')

        folder_counter += 1
        # достаем все файлы из папки
        files = os.listdir(folder)
        # Фильтруем список
        html = filter(lambda x: x.endswith('.html'), files)
        print u'Папка [%s/%s] - %s' % (folder_counter, len(folders), folder)
        print u'Файлов - %s' % len(html)
        print '||'
        print '||'
        print '\/'
        #log.warning(u'Папка [%s/%s] - %s' % (folder_counter, len(folders), folder))
        #log.warning(u'Файлов - %s' % len(html))
        #log.warning('||')
        #log.warning('||')
        #log.warning('\/')

        html_log.warning(u'<p>Папка [%s/%s] - %s ' % (folder_counter, len(folders), folder))
        html_log.warning(u' - Файлов - %s</p>' % len(html))
        html_log.warning('<hr><br>')
        # Начинаем обрабатывать по файлу
        counter = 0
        for page in html:
            counter +=1
            print u"Папка [%s/%s] Файл [%s/%s] название файла: %s" % (folder_counter, len(folders),counter, len(html), folder+'\\'+page)
            #log.warning(u"Папка [%s/%s] Файл [%s/%s] название файла: %s" % (folder_counter, len(folders),counter, len(html), folder+'\\'+page))
            html_log.warning(u"<p>Папка [%s/%s] Файл [%s/%s] название файла: %s</p>" % (folder_counter, len(folders),counter, len(html), folder+'\\'+page))
            # Получаем все ссылки по шаблону из страницы в которой нужно искать
            # так же ссылки типа trener.html, пятый ип обработки.
            links, special = get_links(folder+'\\'+page, template, log, html_log)
            # Переходит по ссылке, качает страницу, сохраняет ее title в словарь
            # Дубликаты удаляются, так как заменятся они все равно будут на одно и то же
            links = links + special
            if links:
                link_text = dict()
                link_text = downloader(links, link_text, log, template, html_log)
                # Ищем идентификаторы для quiz и discuss
                result, double_result, not_found = get_ident(link_text, courses_quiz, courses_discuss, log, html_log)
                # Печатает результаты поиска: ссылка - текст
                print u'Результаты:'
                html_log.warning(u'<p><b>Результаты</b></p><table class="res" border="1" cellpadding="4" cellspacing="1">')
                html_log.warning(u'<tr><td align="center" colspan="3">Результат работы: ссылка - результат (адрес страницы или идентификатор) (дубликаты не учитываются)</td></tr>')
                c = 0
                for k,v in result.items():
                    c += 1
                    print u'[%s] %s - %s' % (c, k, v)
                    #log.warning(u'[%s] %s - %s' % (c, k, v))
                    html_log.warning(u'<tr><td>%s</td><td><a href="%s" target="_blank">%s</a></td><td>%s</td></tr>' % (c, k, k, v))
                html_log.warning('</table>')
                # копируем содержимое оригинального файла в переменную
                with open(folder+'\\'+page) as f:
                    copy = f.read()

                print u'Файл [%s/%s] - обработан. Начинаю замену.' % (counter, len(html))
                #log.warning(u'\nФайл [%s/%s] - обработан. Начинаю замену.' % (counter, len(html)))
                html_log.warning(u'<p>Файл [%s/%s] - обработан. Начинаю замену.</p>' % (counter, len(html)))
                replacer(copy, result, new_folder+'\\'+page, link_text, double_result, not_found, log, html_log)
                print '#'*50
                print '\n'
                #log.warning('#'*50)
                #log.warning('\n')
                html_log.warning('<hr><br>')

        print u'>>> Папка %s обработана.' % folder
        print '#'*50
        print '\n'
        #log.warning(u'>>> Папка %s обработана.' % folder)
        html_log.warning(u'<hr><p>Папка %s обработана.</p>' % folder)
        #log.warning('#'*50)
        #log.warning('\n')

        html_log.warning('</div>\n</body>\n</html>')
