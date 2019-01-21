import cv2
from imageai.Detection import ObjectDetection
import os
from PIL import Image

res = 640

ratio = ((4608)/res)

exec_path = os.getcwd()
object_detect = ObjectDetection()
object_detect.setModelTypeAsRetinaNet()
object_detect.setModelPath( os.path.join(exec_path, "model.h5"))
object_detect.loadModel()

def Direction(crds):
    im = Image.open('clf.jpg')
    width, height = im.size
    avg_w =(crds[0] + crds[2])/2
    avg_h = (crds[1] + crds[3])/2
    w = width/2
    h = height/2
    if avg_w >= w and avg_h <= h:
        txt1 = " is at a slight height towards your right"
    elif avg_w <= w and avg_h <= h:
        txt1 = " is at a slight height towards your left"
    elif avg_w <= w and avg_h >=h:
        txt1 = " is slightly low towards your left"
    elif avg_w >= w and avg_h >= h:
        txt1 = " is slightly low towards your right"
    else:
        txt1 = ""
    return txt1

def Detect(file = "img.jpg"):
    detections = object_detect.detectObjectsFromImage(input_image=os.path.join(exec_path, file), output_image_path=os.path.join(exec_path, "clf.jpg"))
    values = []
    for Object in detections:
        nm = Object["name"]
        crds = Object["box_points"]
        prob = Object["percentage_probability"]
        pixel_dst = crds[2]-crds[1]
        data = [nm, pixel_dst, crds]
        values.append(data)
    return values

#focus_list = [Pixel_width,Actual_dist, Actual_width ]
object_dictionary = {"bottle":[78,36,3.5],
                     "chair":[939,36,20],
                     #"cup":[378/ratio,24,2.5],
                     "laptop":[324,36,14],
                     #"cell phone":[],
                     "keyboard":[381,36,17.5],
                     #"microwave":[2838/ratio,24,19],
                     "person":[468,36,18],
                     #"suitcase":[2198/ratio,24,21],
                     "tv":[786,48,49]}

def Dist(data):
    dist_list = []
    nm_list = []
    txt_list = []
    for each in data:
        obj, pxl_dst, crds = each
        if obj in object_dictionary.keys():
            focus_list = object_dictionary[obj]
            print(focus_list)
            focus = ((int(focus_list[0])*focus_list[1])/focus_list[2])
            distance = ((focus_list[2]*focus)/pxl_dst)/15
            drn_txt = Direction(crds)
        else :
            distance = "na"
            drn_txt = ""
        dist_list.append(distance)
        nm_list.append(obj)
        txt_list.append(drn_txt)

    print(dist_list)
    print(nm_list)
    return (dist_list, nm_list, txt_list)
