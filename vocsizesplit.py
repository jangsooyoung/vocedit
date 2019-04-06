import sys
import PIL
from PIL import Image
from pathlib import Path
import time
from datetime import datetime
import os
import xml.etree.ElementTree as xml_tree
import ntpath

set_debug_level = 0
dest_dir = None
vggsize = 300
overlab = 100


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


class VocEditor:
	def __init__(self):
		self.object_list = []

	def getPartList(self, obj):
		part_list = []
		for o in self.object_list:
			if o.parent == obj:
				part_list.append(o)
		return part_list

	def saveVocXml(self, path_file_name, width, height, object_list):
		log(2, 'saveVocXml()')
		fname = os.path.basename(path_file_name)
		xml = []
		xml.append("<annotation>")
		xml.append("	<folder>carno</folder>")
		xml.append("	<filename>{}</filename>".format(fname.replace('.xml', '.jpg')))
		xml.append("	<source>")
		xml.append("		<database>carno</database>")
		xml.append("		<annotation>carno</annotation>")
		xml.append("		<image>flickr</image>")
		xml.append("	</source>")
		xml.append("	<size>")
		xml.append("		<width>{}</width>".format(int(width)))
		xml.append("		<height>{}</height>".format(int(height)))
		xml.append("		<depth>3</depth>")
		xml.append("	</size>")
		xml.append("	<segmented>0</segmented>")

		for obj in object_list:
			if obj.parent != None:
				continue
			xml.append("	<object>")
			xml.append("		<name>{}</name>".format(obj.name))
			xml.append("		<pose>Unspecified</pose>")
			xml.append("		<truncated>{}</truncated>".format(obj.truncated))
			xml.append("		<difficult>{}</difficult>".format(obj.difficult))
			xml.append("		<bndbox>")
			xml.append("			<xmin>{}</xmin>".format(int(obj.xmin)))
			xml.append("			<ymin>{}</ymin>".format(int(obj.ymin)))
			xml.append("			<xmax>{}</xmax>".format(int(obj.xmax)))
			xml.append("			<ymax>{}</ymax>".format(int(obj.ymax)))
			xml.append("		</bndbox>")
			part_list = self.getPartList(obj)
			for sobj in part_list:
				xml.append("		<part>")
				xml.append("			<name>{}</name>".format(sobj.name))
				xml.append("			<bndbox>")
				xml.append("				<xmin>{}</xmin>".format(int(sobj.xmin)))
				xml.append("				<ymin>{}</ymin>".format(int(sobj.ymin)))
				xml.append("				<xmax>{}</xmax>".format(int(sobj.xmax)))
				xml.append("				<ymax>{}</ymax>".format(int(sobj.ymax)))
				xml.append("			</bndbox>")
				xml.append("		</part>")
			xml.append("	</object>")
		xml.append("</annotation>")

		f = open(path_file_name, "w")
		f.write('\n'.join(xml))
		f.close()
		log(2, 'saveVocXml({} -->())'.format(path_file_name, len(object_list)))

	def findObjTypeBySplitFileLocation(self, fname, obj):
		name = "{}_{}_{}.jpg".format(fname.replace(".jpg", ""), int(obj.xmin), int(obj.ymin))
		log(2, ">>[{}]".format(name))
		for f in all_files:
			log(3, "f[{}]".format(f))
			if f.find(name) > 0:
				log(2, "fname[{}]".format(fname))
				log(2, f)
				dir_objtype = f.split("/")[1]
				log(2, "if {}>{}".format(obj.name, dir_objtype))
				if dir_objtype != obj.name:
					log(0, "CHANGE {}>{}".format(obj.name, dir_objtype))
				obj.name = dir_objtype
		return obj.name

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

	def conv(self, name, dest_dir, vggize):

		img = Image.open(name + ".jpg")
		self.width, self.height, self.object_list = self.loadVocXml(name + ".xml")

		if len(self.object_list) <= 0:
			self.width = img.width
			self.height = img.height

		if self.width <= vggize and self.height < vggsize:
			log(0, name + ".jpg {},{} image size too small".format(self.width, self.height))
			return

		sub_no = 0
		x = 0
		while x + vggsize < self.width:
			y = 0
			while y + vggsize < self.height:
				sub_list = self.extractObject(x, y, x + vggsize, y + vggsize)

				sub_name = "{}/{}_{}".format(dest_dir, self.filenameonly(name), sub_no)
				xmax = min(x + vggsize, self.width)
				ymax = min(y + vggsize, self.height)
				sub_img = img.crop((x, y, xmax, ymax))
				sub_img.save(sub_name + ".jpg")
				if len(self.object_list) > 0 and len(sub_list) > 0:
					self.saveVocXml(sub_name + ".xml", xmax - x, ymax - y, sub_list)
				sub_no += 1
				y += vggsize - overlab
			x += vggsize - overlab

	def extractObject(self, xmin, ymin, xmax, ymax):
		sub_list = []
		for o in self.object_list:
			if xmin <= o.xmin and ymin <= o.ymin and o.xmax <= xmax and o.ymax <= ymax:
				p = o.parent
				if p == None or xmin <= p.xmin and ymin <= p.ymin and p.xmax <= xmax and p.ymax <= ymax:
					sub_o = Obj(o.name, o.xmin - xmin, o.ymin - ymin, o.xmax - xmin, o.ymax - ymin,
								o.truncated, o.difficult, o.objectBox, o.objectNm, o.objectNmBg, o.parent)
					sub_list.append(sub_o)
		return sub_list

	def filenameonly(self, path):
		head, tail = ntpath.split(path)
		return tail or ntpath.basename(head)


if __name__ == '__main__':
	if len(sys.argv) < 5:
		print("python beanimgsplit.py dest_dir vggsize overlab  img_xml_list [-g1]")
		print("	vggsize : 512 or 300")
		print("	overlab : Overlap Average ObjectSize Slightly larger, smaller objects are lost")
		sys.exit(0)

	dest_dir = sys.argv[1]
	vggsize = int(sys.argv[2])
	overlab = int(sys.argv[3])
	flist = sys.argv[4:]
	set_debug_level = 0
	if len(sys.argv) >= 3 and sys.argv[len(sys.argv) - 1].startswith("-g") and len(sys.argv[len(sys.argv) - 1]) >= 2:
		set_debug_level = int(sys.argv[len(sys.argv) - 1][2:])
		flist = flist[:-1]
	log(1, flist)

	voc = VocEditor()
	for fname in flist:
		name = fname.replace(".jpg", "").replace(".xml", "")
		if not Path("{}.jpg".format(name)).is_file():
			log(0, "{}.jpg not found".format(name))
		else:
			voc.conv(name, dest_dir, vggsize)

