Simple VOC Pascal Data Editor <br>
<br>
Configure as concise as possible <br>
The program file can be configured as a single file so that developers can easily rewrite it. <br>
<br>
After reading jpg, display object area and save. <br>
The xml filename is written as jpg name + '.xml'. <br>
<br>
![VOCEDIT](./img/VOC.jpg) <br>
<br>
# Program Manipulation <br>
  python3 vocedit.py jpg_xml_file list <br>
  python3 vocedit_eng.py jpg_xml_file list # English Version <br>
  - At least one Argument must have at least one jpg file. <br>
 Example) python3 vocedit.py * .jpg <br>
<br>
# Create Object <br>
 1. Select object region by dragging <br>
 2. Edit the object name and save it [Enter] <br>
<br>
# Change object name <br>
 1. Double-click on multiple objects <br>
 2. Edit the object name and save it [Enter] <br>
<br>
# Create object part <br>
 1. Select Large Objects <br>
 2. Create an object by dragging inside the object contained in the large object <br>
# Move object name <br>
 l. Select an object and click the arrows <br>
# Resize Object Name <br>
 1. Select the object and Cntl + Arrows <br>
<br>
# Object selection operation <br>
    Select All: Ctl-A <br>
    Unselect all: ESC <br>
    Add selection: left mouse double click <br>
    Uncheck: Right-click <br>
    Delete selection: Del <br>
    Bean autoanalysis: Ctrl-P <br>
    <br>
# File <br>
    Read File: Ctl-R <br>
    Save file: Ctl-U <br>
    Old file: PageUp <br>
    Next file: PageDown <br>
<br>
# Image to organize objects after splitting <br>
  How to verify that object name classification works well <br>
 <br>
 1. python3 vocsplit.py dest_dir img_List <br>
    The voc xml object in img_list is classified and stored by subdirectories with object names. <br>
 <br>
 2. created in dest_dir relocates the image <br>
     The image object, which is called the subdirectory "del", is the object to delete <br>
     Do not modify the generated object file name <br>
     You can modify the XML by modifying the file name <br>
 <br>
 3. python3 vocrenameobk.py dest_dir img_List <br>
    Modify the object name of the XML by reading the list of images divided by dest_dir in vocsplit.py. <br>
