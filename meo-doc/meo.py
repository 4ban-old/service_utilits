# coding: utf-8

import sys
import shutil
import os

meodoc = r'C:\\Users\\PK-DPI-742\\Desktop\\projects\\meo-doc\\html'

public = r'C:\\Users\\PK-DPI-742\\Desktop\\projects\\meo-doc-public'


def copytree(src, dst, symlinks=0):
  print ("copy tree " + src)
  names = os.listdir(src)
  if not os.path.exists(dst):
    os.mkdir(dst)
  for name in names:
    srcname = os.path.join(src, name)
    dstname = os.path.join(dst, name)
    try:
      if symlinks and os.path.islink(srcname):
        linkto = os.readlink(srcname)
        os.symlink(linkto, dstname)
      elif os.path.isdir(srcname):
        copytree(srcname, dstname, symlinks)
      else:
        shutil.copy2(srcname, dstname)
    except (IOError, os.error):
      print ("Can't copy %s to %s: %s", srcname, dstname, str(why))

if __name__ == '__main__':
	dd = os.listdir(public)
	dd.remove('.git')
	for x in dd:
		if x.startswith('_'):
			shutil.rmtree(public+r'\\'+x)
		elif 'sources' == x:
			shutil.rmtree(public+r'\\'+x)
		elif 'static' == x:
			shutil.rmtree(public+r'\\'+x)
		else:
			os.remove(public+r'\\'+x)
	print('Delete all files')
	copytree(meodoc, public)
	dd = os.listdir(public)
	dirs = list()
	files = list()
	for x in dd:
		if x.startswith('_'):
			dirs.append(x)
		elif x.endswith('.html'):
			files.append(x)

	for x in dirs:
		os.rename(public+'\\'+x, public+'\\'+x.replace('_',''))

	for x in files:
		with open(public+'\\'+x, encoding="utf-8") as f:
			text = f.read()
		text = text.replace('href="_static','href="static')
		text = text.replace('href="_sources','href="sources')
		text = text.replace('src="_static','src="static')
		text = text.replace('src="_sources','src="sources')
		with open(public+'\\'+x ,'w', encoding="utf-8") as f:
			f.write(text)