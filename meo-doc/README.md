После дополнения документации запустить
make html && meo.py
Далее
cd Desktop\projects\meo-doc
ga .
gc 'commit'
gp
Далее
cd Desktop\projects\meo-doc-public
ga .
gc 'commit'
gp

Должна существовать папка с инициализированным репозиторием meo-doc-public
на гитхабе должен существовать репозиторий remasik.guthub.io

Настройки создания:
separate source and build directories - yes

=conf.py=
theme - sphinx_rtd_theme
html_static_path = ['_static']

=MAKEFILE=

BUILDDIR      = ./