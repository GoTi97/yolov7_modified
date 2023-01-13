# pip install -r yolov7/requirements.txt
# pip install -r yolov7/requirements_gpu.txt

# python train.py --workers 1 --device 0 --batch-size 16 --epochs 100 --img 640 640 --hyp data/hyp.scratch.custom.yaml --name yolov7-custom --weights yolov7.pt


import json
from pathlib import Path
from PIL import Image
import pandas
import os


def bbox_to_yolo(image_size, bbox):
    dw = 1. / image_size[0]
    dh = 1. / image_size[1]
    x = (bbox['x'] + bbox['x'] + bbox['width']) / 2.0
    y = (bbox['y'] + bbox['y'] + bbox['height']) / 2.0
    w = bbox['width']
    h = bbox['height']
    x = round(x * dw, 6)
    w = round(w * dw, 6)
    y = round(y * dh, 6)
    h = round(h * dh, 6)
    ret_string = "0 " + str(x) + " " + str(y) + " " + str(w) + " " + str(h) + "\n"
    return ret_string


def create_json_to_txt(coco_paths, p_img_paths, p_label_paths, is_train):
    jpg_list = os.listdir(p_img_paths)
    json_list = os.listdir(p_label_paths)
    jpg_list.sort()
    json_list.sort()

    if is_train == 1:
        file_name = "train"
    else:
        file_name = "val"

    g = open(str(coco_paths) + "/" + file_name + ".txt", 'w')
    for jpg_name, label_name in zip(jpg_list, json_list):
        #print(jpg_name, " == ", label_name)
        g.write("./images/" + file_name + "/" + jpg_name + "\n")
        image_size = Image.open(str(p_img_paths) + '/' + jpg_name).size
        bbox_list = json.load(Path(str(p_label_paths)+'/'+label_name).open(mode='r'))
        f = open(str(coco_paths) + "/labels/" + file_name + "/" + jpg_name[0:-4] + ".txt", 'w')
        for bbox in bbox_list:
            f.write(bbox_to_yolo(image_size, bbox))
        f.close()
    g.close()
    return 0


Train_Image_Path = Path('/home/development/users/dongyeon/datamaker/yolov7/coco/images/train')
Train_Label_Path = Path('/home/development/users/dongyeon/datamaker/yolov7/coco/labels/train_json')
Val_Image_Path = Path('/home/development/users/dongyeon/datamaker/yolov7/coco/images/val')
Val_Label_Path = Path('/home/development/users/dongyeon/datamaker/yolov7/coco/labels/val_json')
coco_Path = Path('/home/development/users/dongyeon/datamaker/yolov7/coco')

coco_bak_Path = Path('/home/development/users/dongyeon/datamaker/yolov7/coco_bak')
test_Image_Path = Path('/home/development/users/dongyeon/datamaker/yolov7/coco_bak/images/train')
test_Label_Path = Path('/home/development/users/dongyeon/datamaker/yolov7/coco_bak/labels/train')
#create_json_to_txt(coco_bak_Path, test_Image_Path, test_Label_Path, 1)

create_json_to_txt(coco_Path, Train_Image_Path, Train_Label_Path, 1)
create_json_to_txt(coco_Path, Val_Image_Path, Val_Label_Path, 0)


#path_to_txt = Path('/home/development/users/dongyeon/datamaker/yolov7/coco/train.txt')

#jpg_list = os.listdir(Train_Image_Path)
#json_list = os.listdir(Train_Label_Path)

# with open('/home/development/users/dongyeon/datamaker/yolov7/coco/train.txt', 'r') as r:
#     for line in sorted(r):
#         print(line, end='')

#image_object = Image.open('/home/development/users/dongyeon/datamaker/yolov7/coco/images/train/airport_inside_airport_inside_0007.jpg')
#image_size = image_object.size

#list = json.load(Path(str(Train_Label_Path)+'/'+json_list[0]).open(mode='r'))
#for bbox in list:
    #print(bbox_to_yolo(image_size,bbox))

#ret = "0 0.3 0.3 0.3"



#empty 파일 갯수 세는 코드
# train_Label_Path = Path('/home/development/users/dongyeon/datamaker/yolov7/coco/labels/val_json')
# json_list = os.listdir(train_Label_Path)
# cnt = 0
# for file_name in json_list:
#     bbox_list = json.load(Path(str(train_Label_Path)+'/'+file_name).open(mode='r'))
#     if len(bbox_list) == 0:
#        cnt += 1
# print(cnt)

