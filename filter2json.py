import json
import os
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--coco_anno', default=r"COCO_dataset\annotations\instances_train2017.json", type=str, help='The path for instances_train/val2017 in the COCO Dataset.')
parser.add_argument('--coco_img', default=r"COCO_dataset\images", type=str, help='The image paths for the COCO Dataset.')
parser.add_argument('--json_anno', default=r"output.json", type=str, help='The JSON format annotation files to be exported.')
parser.add_argument('--json_img', default=r"output_img", type=str, help='The images corresponding to the annotation files.')
parser.add_argument('--classes', nargs='+', type=int, default=[1], help='Class numbers separated by spaces, e.g., 1 2 3.')

args = parser.parse_args()

# ! 讀取COCO instances_(train/val)2017.json, 儲存成Dict
with open(args.coco_anno, 'r') as load_f:
    json_dict = json.load(load_f)

# ! 提取出類別要存放的新Dict
new_json_dict = {
    "info": {'description': 'COCO 2017 Person Dataset', 'url': 'https://github.com/KennyChen880127', 'version': '1.0', 'year': 2024, 'contributor': 'Kenny Chen', 'date_created': '2024/04/28'},
    "licenses": json_dict["licenses"],
    "images": [],
    "annotations": [],
    "categories": [{'supercategory': 'appliance', 'id': 80, 'name': 'oven'}]
}

os.makedirs(args.json_img, exist_ok=True)

img_id_list = []

for id in args.classes:
    for an in json_dict['annotations']:
        # ! an type is dict
        if an['category_id'] == id:
            new_json_dict['annotations'].append(an) # ! 將指定類別的annotations資料加入list
            
            # ! 將指定類別圖片移至新路徑
            for image in json_dict['images']:
                if image['id'] == an['image_id']:
                    shutil.copy(os.path.join(args.coco_img, image['file_name']), os.path.join(args.json_img, image['file_name']))

                    if image['id'] not in img_id_list:
                        img_id_list.append(image['id'])
                        new_json_dict['images'].append(image)
                        
                    break

with open(args.json_anno, 'w') as save_f:
    json.dump(new_json_dict, save_f)
