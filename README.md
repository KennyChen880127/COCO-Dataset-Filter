<div align="center">
<h1>
<b>
COCO-Dataset-Filter
</b>
</h1>
</div>

This repository will extract specified categories from the COCO Dataset and save them in YOLO format.
 
# COCO Dataset
[COCO](https://cocodataset.org/#home) is a large-scale object detection, segmentation, and captioning dataset. COCO has several features:

* Object segmentation
* Recognition in context
* Superpixel stuff segmentation
* 330K images (>200K labeled)
* 1.5 million object instances
* 80 object categories
* 91 stuff categories
* 5 captions per image
* 250,000 people with keypoints
  
## Steps to run Code
* Clone the repository

        git clone https://github.com/KennyChen880127/COCO-Dataset-Filter.git

* Download the COCO dataset and the 2017 annotations.(instances_(train/val)2017.json)

        sh data/COCO.sh

* Run a Python script.

        python filter.py --coco_anno COCO_dataset/annotations --coco_img COCO_dataset/images --yolo_label datasets/labels/train --yolo_img datasets/images/train --classes 1 2 3 # person, bicycle, car

  - --coco_anno: The path for instances_train/val2017 in the COCO Dataset.
  - --coco_img: The image paths for the COCO Dataset.
  - --yolo_label: The YOLO annotation files to be exported
  - --yolo_img: The images corresponding to the annotation files to be exported.
  - --classes: Class numbers separated by spaces, e.g., 1 2 3.

* You can refer to coco_classes.txt for class IDs.
