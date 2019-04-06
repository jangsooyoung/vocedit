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


class VocSplit:
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

		log(2, 'loadVocXml({})'.format(file_name))
		object_list = []
		tree = xml_tree.parse(file_name)
		root = tree.getroot()
		# Image shape.
		size = root.find('size')
		shape = [int(size.find('height').text), int(size.find('width').text), int(size.find('depth').text)]
		# Find annotations.
		for xml_obj in root.findall('object'):
			label = xml_obj.find('name').text
			difficult_val = xml_obj.find('difficult').text
			truncated_val = xml_obj.find('truncated').text
			bbox = xml_obj.find('bndbox')
			obj = Obj(label, float(bbox.find('xmin').text), float(bbox.find('ymin').text),
					  float(bbox.find('xmax').text), float(bbox.find('ymax').text),
					  truncated=truncated_val, difficult=difficult_val)
			object_list.append(obj)
			for part in xml_obj.findall('part'):
				p_label = part.find('name').text
				p_bbox = part.find('bndbox')
				p_obj = Obj(p_label, float(p_bbox.find('xmin').text), float(p_bbox.find('ymin').text),
							float(p_bbox.find('xmax').text), float(p_bbox.find('ymax').text),
							parent=obj)
				object_list.append(p_obj)

		return int(size.find('width').text), int(size.find('height').text), object_list

	def filenameonly(self, path):
	    head, tail = ntpath.split(path)
	    return tail or ntpath.basename(head)

	def subImageByRect(self, img, o):
		#return img[int(o.ymin):int(o.ymax), int(o.xmin):int(o.xmax)]
		w = len(img[0])
		h = len(img)
		g = 15
		x = int(o.xmin) - g
		y = int(o.ymin)  - g
		x1 = int(o.xmax) + g
		y1 = int(o.ymax) + g

		if x < 0  : x = 0
		if y < 0  : y = 0
		if w < x1 : x1 = w -1
		if h < y1 : y1 = h - 1

		return img[y:y1, x:x1]

	def split(self, fname, dest_dir):
		log(0, fname)
		self.width, self.height, self.object_list = self.loadVocXml(fname.replace(".jpg", ".xml"))
		img = cv2.imread(fname)
		fname1 = self.filenameonly(fname).replace(".jpg", "")
		for o in self.object_list:
			sub_img = self.subImageByRect(img, o)
			sub_dir = "{}/{}".format(dest_dir, o.name)
			self.mkdir(sub_dir)
			sub_fname = "{}/{}_{}_{}.jpg".format(sub_dir,fname1, int(o.xmin), int(o.ymin))
			log(1, sub_fname)
			cv2.imwrite(sub_fname, sub_img)

	def mkdir(self, dir):
		try:
			os.stat(dir)
		except:
			os.mkdir(dir)  

if __name__ == '__main__':

	if len(sys.argv) <= 2:
		print("python3 vocsplit.py dest_dir image_list [-g1]")
		sys.exit(1)

	dest_dir = sys.argv[1]
	flist = sys.argv[2:]
	set_debug_level = 0
	if len(sys.argv) >= 3 and sys.argv[len(sys.argv) - 1].startswith("-g") and len(sys.argv[len(sys.argv) - 1]) >= 2:
		set_debug_level = int(sys.argv[len(sys.argv) - 1][2:])
		flist = flist[:-1]
	log(1, flist)
	voc = VocSplit()
	for fname in flist:
		voc.split(fname, dest_dir)
