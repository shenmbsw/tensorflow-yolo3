import os
import random
import shutil
from tqdm import tqdm

def image_migrate(XmlPath,pictureBasePath,saveBasePath):
    total_xml = os.listdir(XmlPath)
    num = len(total_xml)
    if os.path.exists(saveBasePath) == False:
        os.makedirs(saveBasePath)
    print('Moving image into dataset')
    for xml in tqdm(total_xml):
        folder = 'MVI_' + xml[:5]
        temp_pictureBasePath = os.path.join(pictureBasePath, folder)
        filename = 'img' + xml[5:10] + ".jpg"
        filePath = os.path.join(temp_pictureBasePath, filename)
        newfile = xml.split(".")[0] + ".jpg"
        newfile_path = os.path.join(saveBasePath, newfile)
        shutil.copyfile(filePath, newfile_path)
    print("xml file total number", num)

def get_train_list(MVI_ImagePath,val_video_num):
    total_MVI = os.listdir(MVI_ImagePath)
    num_MVI = len(total_MVI)
    list_MVI = range(num_MVI)
    MVI = []
    for i in list_MVI:
        name = total_MVI[i][4:]
        if name not in MVI:
            MVI.append(name)
    MVI_val = random.sample(MVI,val_video_num)
    MVI_train = []
    for i in MVI:
        if i not in MVI_val:
            MVI_train.append(i)
    return MVI_train, MVI_val

def write_txt(xmlfilepath, saveBasePath, MVI_ImagePath,val_video_num=5):
    print('saperating train val dataset')
    total_xml = os.listdir(xmlfilepath)
    num = len(total_xml)
    list = range(num)
    MVI_train, MVI_val = get_train_list(MVI_ImagePath,val_video_num)
    if os.path.exists(saveBasePath) == False:
        os.makedirs(saveBasePath)
    ftrainval = open(os.path.join(saveBasePath, 'trainval.txt'), 'w')
    ftrain = open(os.path.join(saveBasePath, 'train.txt'), 'w')
    fval = open(os.path.join(saveBasePath, 'val.txt'), 'w')
    for i in list:
        name_MVI = total_xml[i][:5]
        name = total_xml[i][:-4] + '\n'
        ftrainval.write(name)
        if name_MVI in MVI_train:
            ftrain.write(name)
        else:
            fval.write(name)
    ftrain.close()
    ftrainval.close()
    fval.close()
    print('done')

if __name__ == '__main__':
    import config
    image_migrate(config.xmlpath,config.ImageBasePath,config.imagepath)
    write_txt(config.xmlpath, config.txtpath, config.ImageBasePath, config.val_video_num)
