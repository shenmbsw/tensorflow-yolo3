# tensorflow-yolo3

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)

# Setup environment

1. virtualenv --python=python3.5 py35
2. source py35/bin/activate
3. cd [dir of tf-yolo3]
4. pip install -r requirements.txt


---
## Data Prepare
1. Download the DETRAC dataset from [detrac_website](http://detrac-db.rit.albany.edu/download)  
2. chage the config.py file to the location of your downloaded dataset.  
3. run script in data to parse XML file.
```
cd datasets
python XML_parser.py
python image_migrate.py  
```  

## Training

1. If you want to use original pretrained weights for YOLOv3, download from [darknet53 weights](https://pjreddie.com/media/files/darknet53.conv.74)   
2. rename it as darknet53.weights, and modify the darknet53_weights_path in the config.py 

```
wget https://pjreddie.com/media/files/darknet53.conv.74`  
```  
3. Modify the data augmentation parameters and train parameters  
4. Run yolo_train.py  

## Evaluation
1. Modify the pre_train_yolo3 and model_dir in config.py  
2. Run detect.py  

```
python detect.py --image_file ./test.jpg
```

## Notice

If you want to modify the Gpu index, please modify gpu_index in config.py

## Credit
```
@article{yolov3,
	title={YOLOv3: An Incremental Improvement},
	author={Redmon, Joseph and Farhadi, Ali},
	journal = {arXiv},
	year={2018}
}
```

## Reference
* [keras-yolo3](https://github.com/qqwweee/keras-yolo3)
* [tf-yolo3](https://github.com/aloyschen/tensorflow-yolo3)
