import json
import os
import shutil
import argparse

coco_classes =  [
    "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat", "trafficlight",
    "firehydrant", "streetsign", "stopsign", "parkingmeter", "bench", "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe", "hat", "backpack", "umbrella", "shoe", "eyeglasses",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sportsball", "kite", "baseballbat",
    "baseballglove", "skateboard", "surfboard", "tennisracket", "bottle", "plate", "wineglass", "cup", "fork",
    "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hotdog", "pizza",
    "donut", "cake", "chair", "sofa", "pottedplant", "bed", "mirror", "diningtable", "window", "desk", "toilet",
    "door", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cellphone", "microwave", "oven", "toaster",
    "sink", "refrigerator", "blender", "book", "clock", "vase", "scissors", "teddybear", "hairdrier",
    "toothbrush", "hairbrush"
    ]

# ! Parser definition, convenient for CLI operation, if you want to operate in VSCode, please change default
parser = argparse.ArgumentParser()
parser.add_argument('--ca', '--coco_anno', default=r"COCO_dataset\annotations\instances_train2017.json", type=str, help='The path for instances_train/val2017 in the COCO Dataset.')
parser.add_argument('--ci', '--coco_img', default=r"COCO_dataset\images", type=str, help='The image paths for the COCO Dataset.')
parser.add_argument('--yl', '--yolo_label', default=r"labels\train", type=str, help='The YOLO annotation files to be exported.')
parser.add_argument('--yi', '--yolo_img', default=r"images\train", type=str, help='The images corresponding to the annotation files to be exported.')
parser.add_argument('--cls', '--classes', nargs='+', type=int, default=[1], help='Class numbers separated by spaces, e.g., 1 2 3.')
args = parser.parse_args()

# ! Create folders to store output YOLO annotation files and images
os.makedirs(args.yolo_img, exist_ok=True) # ! Corresponding images
os.makedirs(args.yolo_label, exist_ok=True) # ! Create output YOLO format text files

##################
##### Filter #####
##################
# ! Read COCO instances_(train/val)2017.json and save it as a Dict
with open(args.coco_anno, 'r') as load_f:
    json_dict = json.load(load_f)

img_id_list = []

# ! Extract new Dict for categories to be stored
new_json_dict = {
    "info": {'description': 'COCO 2017 Person Dataset', 'url': 'https://github.com/KennyChen880127', 'version': '1.0', 'year': 2024, 'contributor': 'Kenny Chen', 'date_created': '2024/04/28'},
    "licenses": json_dict["licenses"],
    "images": [],
    "annotations": [],
    "categories": [{'supercategory': 'None', 'id': None, 'name': 'None'}]
}

# ! Make new Dict and export images
for id in args.classes: # * Store as many times as there are categories
    for an in json_dict['annotations']:
        # ! an type is dict
        if an['category_id'] == id:
            new_json_dict['annotations'].append(an) # ! Add annotations data of specified categories to the list
            
            # ! Move images of specified categories to new path
            for image in json_dict['images']:
                if image['id'] == an['image_id']:
                    shutil.copy(os.path.join(args.coco_img, image['file_name']), os.path.join(args.yolo_img, image['file_name']))
                    
                    if image['id'] not in img_id_list:
                        img_id_list.append(image['id'])
                        new_json_dict['images'].append(image)

                    break

#################
##### YOLO ######
#################
classes_id_list = [] # Store class IDs in the List
# ! Create classes.txt
for an in new_json_dict["annotations"]:
    if an['category_id'] not in classes_id_list:
        classes_id_list.append(an['category_id'])
classes_id_list.sort()

with open(f"{args.yolo_label}/classes.txt", 'w') as f:
    for i in classes_id_list:
        f.write(f"{coco_classes[i-1]}\n")

# ! Convert json to COCO
for image in new_json_dict['images']:
    text_list = [] # 
    for annotation in new_json_dict['annotations']:         
        if image['id'] == annotation['image_id']:

            image_width = image['width']
            image_height = image['height']

            bbox = annotation['bbox']
            x, y, width, height = bbox
            
            # Calculate the relative position of the object center
            x_center = (x + width / 2) / image_width
            y_center = (y + height / 2) / image_height
            
            # Calculate the relative proportions of the width and height of the object
            relative_width = width / image_width
            relative_height = height / image_height

            txt_name = image['file_name'].split(".")
            text_list.append(f"{classes_id_list.index(annotation['category_id'])} {round(x_center, 6)} {round(y_center, 6)} {round(relative_width, 6)} {round(relative_height, 6)}")
            
            with open(f"{args.yolo_label}/{txt_name[0]}.txt", 'a') as f:
                for text in text_list:
                    f.write(text + '\n')
