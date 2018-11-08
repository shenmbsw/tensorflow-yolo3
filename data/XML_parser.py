import xml.etree.ElementTree as ET
from xml.dom.minidom import Document
import os
import cv2
import time


def ConvertVOCXml(file_path="", file_name=""):
    tree = ET.parse(file_name)
    root = tree.getroot()
    # print(root.tag)

    num = 0

    frame_lists = []
    output_file_name = ""
    for child in root:

        if (child.tag == "frame"):

            doc = Document()
            annotation = doc.createElement('annotation')
            doc.appendChild(annotation)

            # print(child.tag, child.attrib["num"])
            pic_id = child.attrib["num"].zfill(5)
            # print(pic_id)
            # output_file_name=root.attrib["name"]+"__img"+pic_id+".xml"
            output_file_name = root.attrib["name"][-5:] + pic_id + ".xml"
            # print(output_file_name)

            folder = doc.createElement("folder")
            folder.appendChild(doc.createTextNode("VOC2007"))
            annotation.appendChild(folder)

            filename = doc.createElement("filename")
            pic_name = "img" + pic_id + ".jpg"
            filename.appendChild(doc.createTextNode(pic_name))
            annotation.appendChild(filename)

            sizeimage = doc.createElement("size")
            imagewidth = doc.createElement("width")
            imageheight = doc.createElement("height")
            imagedepth = doc.createElement("depth")

            imagewidth.appendChild(doc.createTextNode("960"))
            imageheight.appendChild(doc.createTextNode("540"))
            imagedepth.appendChild(doc.createTextNode("3"))

            sizeimage.appendChild(imagedepth)
            sizeimage.appendChild(imagewidth)
            sizeimage.appendChild(imageheight)
            annotation.appendChild(sizeimage)

            target_list = child.getchildren()[0]
            # print(target_list.tag)
            object = None
            for target in target_list:
                if (target.tag == "target"):
                    # print(target.tag)
                    object = doc.createElement('object')
                    bndbox = doc.createElement("bndbox")

                    for target_child in target:
                        if (target_child.tag == "box"):
                            xmin = doc.createElement("xmin")
                            ymin = doc.createElement("ymin")
                            xmax = doc.createElement("xmax")
                            ymax = doc.createElement("ymax")
                            xmin_value = int(float(target_child.attrib["left"]))
                            ymin_value = int(float(target_child.attrib["top"]))
                            box_width_value = int(float(target_child.attrib["width"]))
                            box_height_value = int(float(target_child.attrib["height"]))
                            xmin.appendChild(doc.createTextNode(str(xmin_value)))
                            ymin.appendChild(doc.createTextNode(str(ymin_value)))
                            if (xmin_value + box_width_value > 960):
                                xmax.appendChild(doc.createTextNode(str(960)))
                            else:
                                xmax.appendChild(doc.createTextNode(str(xmin_value + box_width_value)))
                            if (ymin_value + box_height_value > 540):
                                ymax.appendChild(doc.createTextNode(str(540)))
                            else:
                                ymax.appendChild(doc.createTextNode(str(ymin_value + box_height_value)))

                        if (target_child.tag == "attribute"):
                            name = doc.createElement('name')
                            pose = doc.createElement('pose')
                            truncated = doc.createElement('truncated')
                            difficult = doc.createElement('difficult')

                            typename = target_child.attrib['vehicle_type']
                            name.appendChild(doc.createTextNode(typename))
                            pose.appendChild(doc.createTextNode("Left"))
                            truncated.appendChild(doc.createTextNode("0"))
                            difficult.appendChild(doc.createTextNode("0"))

                            object.appendChild(name)
                            object.appendChild(pose)
                            object.appendChild(truncated)
                            object.appendChild(difficult)

                    bndbox.appendChild(xmin)
                    bndbox.appendChild(ymin)
                    bndbox.appendChild(xmax)
                    bndbox.appendChild(ymax)
                    object.appendChild(bndbox)
                    annotation.appendChild(object)

            file_path_out = os.path.join(file_path, output_file_name)
            f = open(file_path_out, 'w')
            f.write(doc.toprettyxml(indent=' ' * 4))
            f.close()
            num = num + 1
    return num

def bboxes_draw_on_img(img, bbox, color=[255, 0, 0], thickness=2):
    # Draw bounding box...
    print(bbox)
    p1 = (int(float(bbox["xmin"])), int(float(bbox["ymin"])))
    p2 = (int(float(bbox["xmax"])), int(float(bbox["ymax"])))
    cv2.rectangle(img, p1, p2, color, thickness)

def visualization_image(image_name, xml_file_name):
    tree = ET.parse(xml_file_name)

    root = tree.getroot()

    object_lists = []
    for child in root:
        if (child.tag == "folder"):
            print(child.tag, child.text)
        elif (child.tag == "filename"):
            print(child.tag, child.text)
        elif (child.tag == "size"):  # 解析size
            for size_child in child:
                if (size_child.tag == "width"):
                    print(size_child.tag, size_child.text)
                elif (size_child.tag == "height"):
                    print(size_child.tag, size_child.text)
                elif (size_child.tag == "depth"):
                    print(size_child.tag, size_child.text)
        elif (child.tag == "object"):  # 解析object
            singleObject = {}
            for object_child in child:
                if (object_child.tag == "name"):
                    # print(object_child.tag,object_child.text)
                    singleObject["name"] = object_child.text
                elif (object_child.tag == "bndbox"):
                    for bndbox_child in object_child:
                        if (bndbox_child.tag == "xmin"):
                            singleObject["xmin"] = bndbox_child.text
                            # print(bndbox_child.tag, bndbox_child.text)
                        elif (bndbox_child.tag == "ymin"):
                            # print(bndbox_child.tag, bndbox_child.text)
                            singleObject["ymin"] = bndbox_child.text
                        elif (bndbox_child.tag == "xmax"):
                            singleObject["xmax"] = bndbox_child.text
                        elif (bndbox_child.tag == "ymax"):
                            singleObject["ymax"] = bndbox_child.text
            object_length = len(singleObject)
            if (object_length > 0):
                object_lists.append(singleObject)

    img = cv2.imread(image_name)

    for object_coordinate in object_lists:
        bboxes_draw_on_img(img,object_coordinate)
    cv2.imwrite("a.jpg", img)


def convert(source_path, save_path, log_path=None):
    totalxml = os.listdir(source_path)
    total_num = 0
    flag = False
    print("start converting XML file")
    if os.path.exists(save_path) == False:
        os.makedirs(save_path)
    # Start time
    start = time.time()
    for xml in totalxml:
        file_name = os.path.join(source_path, xml)
        print("converting {}".format(file_name))
        num = ConvertVOCXml(file_path=save_path, file_name=file_name)
        total_num = total_num + num
    # End time
    end = time.time()
    seconds = end - start
    print("overall {a} object, time taken : {b} seconds".format(a=total_num,b=seconds))
    


if (__name__ == "__main__"):
    import config
    convert(config.XMLBasePath,config.xmlpath)
    # visualization_image("/homeb/liyh/Dataset/DETRAC/Insight-MVT_Annotation_Train/MVI_40212/img00396.jpg",
    #                     "/homeb/liyh/shenshen/ObjectDetection/data/VOC2007/Annotations/MVI_40212__img00396.xml")
