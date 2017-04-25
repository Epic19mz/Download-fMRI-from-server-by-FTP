#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
"""

Usage:
  FTPImageConvert.py

  如有疑问，请联系作者：苗震 epic19mz@mail.ustc.edu.cn
  If you have any question, please contact Zhen MIAO by email. epic19mz@mail.ustc.edu.cn
  
"""

import os
import sys
import shutil
import logging
import dicom
import time

from ftplib import FTP
from docopt import docopt	

def download(ftp,newfiles,Path):
	for filename in newfiles:
		local_filename=os.path.join("E:\\temp",filename)	#直接下载文件储存地址
		print(local_filename)
		file_handler = open(local_filename, 'wb' )
		ftp.retrbinary('RETR %s' % (filename),file_handler.write)
		file_handler.close()
		dcm = dicom.read_file(local_filename)
		dirname = "run1"	#文件夹名称
		print(Path)
		dest_dir = os.path.join(Path,dirname)
		if not os.path.isdir(dest_dir):
			logging.info("Creating directory: {0}".format(dest_dir))
			os.makedirs(dest_dir)
		dest_filename = "{0:09d}.dcm".format(dcm.InstanceNumber)
		dest_file= os.path.join(dest_dir, dest_filename)
		shutil.copy(local_filename, dest_file)
		print("Success")
	
	
	

def main(arguments):
	log_level = logging.INFO
	ftp=FTP()
	ftp.set_debuglevel(2)
	ftp=FTP()
	ftp.connect('192.168.4.4',21)	#IP地址及端口
	ftp.login('sdc','adw2.0')	#用户名及密码
	bufsize = 1024*100
	i1=0
	for i in range(10000) :
		try :
			ftp.cwd('//export//home1//sdc_image_pool//images//p173//e860//s6598')	#主机文件夹目录
			i1=1
			break
		except :
			time.sleep(0.01)
	if i1 == 0 :
		print("There is no file")
		sys.exit(0)
	downloaded=list()
	Path="E:\neurofeedback_test\GE\s1"
	for i in range(5000) :
		files=list()
		ftp.retrlines('NLST',callback=files.append)
		n=len(files)-len(downloaded)
		if n > 0 :
			newfiles=files[-n:]
			download(ftp,newfiles,Path)
			print("Download %d files",n)
		else :
			print("There is no new files.")
			time.sleep(0.1)
		downloaded=files
	
if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
