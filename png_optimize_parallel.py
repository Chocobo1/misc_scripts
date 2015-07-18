#!/bin/python2
"""
Chocobo1 (Mike Tzou), 2015
"""

import os, sys, shutil, subprocess, multiprocessing


class ProgressBar(object):
	def __init__(self, t):
		self.bar_size = 20
		self.total = t
		self.num = 0  # TODO: make this variable share between process

	def print_progress(self):
		r = float(self.num) / self.total
		self.num += 1
		bar = ('#' * int(r * self.bar_size)).ljust(self.bar_size, ' ')
		print "\r  [%s]  %.1f%%" % (bar, r * 100),


def prepare(work_path , orig_name , tmp_name):
	import tempfile
	tmp_path = tempfile.mkdtemp(dir = work_path)
	shutil.copy2(orig_name, os.path.join(tmp_path, tmp_name))
	open(os.path.join(tmp_path, orig_name), 'a').close()  # create a empty file to track current working file
	return tmp_path


def cleanup(new_name, tmp_path , orig_name):
	shutil.move(os.path.join(tmp_path, new_name), os.path.splitext(orig_name)[0] + ".png")
	shutil.rmtree(tmp_path)


def helper_optipng(d):
	tmp_name = "orig_img"
	newfile_name = "new_img.png"
	tmp_dir = prepare(d['img_dir'] , d['img_name'] , tmp_name)
	subprocess.call(["optipng" , "-quiet" , "-preserve" , "-o4" , os.path.join(tmp_dir, tmp_name) , "-out" , os.path.join(tmp_dir, newfile_name)])
	cleanup( newfile_name , tmp_dir , d['img_name'])
#	d['progress_bar'].print_progress()


def helper_pngout(d):
	tmp_name = "orig_img"
	newfile_name = "new_img.png"
	tmp_dir = prepare(d['img_dir'] , d['img_name'] , tmp_name)
	subprocess.call(["pngout" , os.path.join(tmp_dir, tmp_name) , os.path.join(tmp_dir, newfile_name) , "/q"])
	subprocess.call(["DeflOpt" , "/s" , "/d" , os.path.join(tmp_dir, newfile_name)])
	cleanup( newfile_name , tmp_dir , d['img_name'])
#	d['progress_bar'].print_progress()


def helper_job( func , dir_path , file_ext , count ):
	import datetime

	proc_num = None  # defaults to all available cores on runtime
	chunk_size = 1

	file_list = filter( lambda x: x.endswith(file_ext) , os.listdir(dir_path) )
	p = ProgressBar(len(file_list))
	file_dict = reduce( lambda x, y: x + [{'img_name' : y , 'img_dir' : cur_path , 'progress_bar' : p }] , file_list , [] )
	print "Stage %d, processing %d files" % (count , len(file_list))

	pool = multiprocessing.Pool(processes = proc_num)
#	p.print_progress()

	start_time = datetime.datetime.now()
	pool.map(func , file_dict , chunk_size)
	pool.close()
	pool.join()
	print "\nTime spent: " , (datetime.datetime.now() - start_time)
	print "Stage %d, finished\n" % count


def py2exe_pack():
#	import py2exe, distutils
	distutils.core.setup(console=['run.py'])


import time
if __name__ == '__main__':
	multiprocessing.freeze_support()  # for py2exe, otherwise this script is fork-bomb

	stage_count = 1
	cur_path = os.path.dirname(os.path.abspath(sys.argv[0]))  # this script location

	helper_job( helper_optipng , cur_path , ".bmp" , stage_count )
	stage_count += 1

	helper_job( helper_pngout , cur_path , ".png" , stage_count )
	stage_count += 1
