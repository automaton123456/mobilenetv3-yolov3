import xml.etree.ElementTree as ET

classes = ["fullgolfclub", "golfball", "golfclub", "golfer", "golfer_front"]

#Write out our classes file
classes_file = open('model_data/voc_classes.txt', 'w')
classes_file.truncate(0)

for myclass in classes:
  classes_file.write(myclass + "\n")

classes_file.close()

def convert_annotation(xml, list_file):
    in_file = open(xml)
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(float(xmlbox.find('xmin').text)), 
        int(float(xmlbox.find('ymin').text)), 
        int(float(xmlbox.find('xmax').text)), 
        int(float(xmlbox.find('ymax').text)))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))


import glob
import os

all_files = glob.glob("/content/mobilenetv3-yolov3/AllDataStripped/*/*/*.xml")

list_file = open('train.txt', 'w')

for xml in all_files:
  file, ext = os.path.splitext(xml)
  
  jpg_file = file + ".jpg"
  if not os.path.exists(jpg_file):
    continue

  jpg_file_no_space = jpg_file.replace(' ','_')
  os.rename(jpg_file, jpg_file_no_space)

  list_file.write(jpg_file_no_space)
  convert_annotation(xml, list_file)
  list_file.write('\n')

list_file.close()

