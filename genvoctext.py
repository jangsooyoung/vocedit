import simpleguitk
from tkinter import *
from tkinter import messagebox
import time
from PIL import ImageTk, Image
import xml.etree.ElementTree as xml_tree
import os.path
import cv2
import numpy
import time
from datetime import datetime
import ntpath

set_debug_level = 0

def log(debug, s):
	global set_debug_level
	if debug > set_debug_level:
		return
	print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], s)


class Obj:
	def __init__(self, name, xmin, ymin, xmax, ymax, truncated=0, difficult=0, objectBox=None, objectNm=None,
				 objectNmBg=None, parent=None):
		self.name = name 
		self.xmin = xmin 
		self.ymin = ymin
		self.xmax = xmax
		self.ymax = ymax
		self.truncated = truncated
		self.difficult = difficult
		self.objectBox = objectBox
		self.objectNm = objectNm
		self.objectNmBg = objectNmBg
		self.parent = parent


class VocConv:
	def __init__(self):
		self.object_list = []

	def getPartList(self, obj):
		part_list = []
		for o in self.object_list:
			if o.parent == obj:
				part_list.append(o)
		return part_list

	def loadVocXml(self, file_name):
		if not os.path.isfile(file_name):
			return 0, 0, []

		tree = xml_tree.parse(file_name)
		root = tree.getroot()
		find_object_list = []	
		for xml_obj in root.findall('object'):
			oname = xml_obj.find('name').text
			if oname not in find_object_list:
				find_object_list.append(oname)
			for part in xml_obj.findall('part'):
				oname =part.find('name').text
				if oname not in find_object_list:
					find_object_list.append(oname)

		fnm = "{}".format(self.getfilename(fname.replace('.xml', '')))
		for o in find_object_list:
			self.append("{}.txt".format(o), "{} 1\n".format(fnm))
		if len(find_object_list)>0:
			self.append("{}.txt".format(gb), "{}\n".format(fnm))

	def conv(self, fname):
		self.loadVocXml(fname)
		if len(self.object_list) > 0:
			self.append("{}.txt".format(gb), "{}\n".format(self.getfilename(fname.replace('.xml', ''))))

	def append(self, fname, text)		:
		with open("{}/{}".format(dest_dir, fname), "a+") as fp:
			fp.write(text)

	def getfilename(self, path):
		head, tail = ntpath.split(path)
		return tail or ntpath.basename(head)
if __name__ == '__main__':
	if len(sys.argv) <= 3:
		print("python3 genvoctxt.py dest_dir gb image_list [-g0]")
		print("		gb : test , trainval, ..")

	
	dest_dir = sys.argv[1]
	gb       = sys.argv[2]
	flist = sys.argv[3:]
	set_debug_level = 0
	if len(sys.argv) >= 4 and sys.argv[len(sys.argv) - 1].startswith("-g") and len(sys.argv[len(sys.argv) - 1]) >= 2:
		set_debug_level = int(sys.argv[len(sys.argv) - 1][2:])
		flist = flist[:-1]
	log(1, flist)

	voc = VocConv()
	for fname in flist:
		try:
			voc.conv(fname)
		except Exception as e:
			print(fname, e)
