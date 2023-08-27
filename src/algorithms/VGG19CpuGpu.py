import os
import numpy as np
from collections import Counter

from PIL import Image
import csv
import torch
import torch.nn
import torchvision.models as models
import torch.cuda
import torchvision.transforms as transforms
from torchvision import transforms
from .wordcloud2frame import wordfrequency,plotwordcloud


transform = transforms.Compose([           
 transforms.Resize(256),                    
 transforms.CenterCrop(224),                
 transforms.ToTensor(),                     
 transforms.Normalize(                      
 mean=[0.485, 0.456, 0.406],                
 std=[0.229, 0.224, 0.225]                  
 )])

 
def make_model():
    model=models.vgg19(pretrained = True)
    model=model.eval()	
    if(torch.cuda.is_available()):#判断torch是否支持gpu
        model.cuda()	
    return model

def objectDetection(imagepath):
    model=make_model()#选cpu还是gpu
    if imagepath is None or imagepath == '':
       return
    #file_list = os.listdir(r"../../img/ruancai")# 获取给定文件夹下的所有文件名
    print(os.getcwd())
    print(imagepath)
    file_list=os.listdir(imagepath)

    framelist = []
    with open('./src/algorithms/imagenet_classes.txt') as f:
        classes = [line.strip() for line in f.readlines()]
    # 遍历文件名列表
    for file_name in file_list:
        # 判断文件是否是图片
        if os.path.splitext(file_name)[-1] in ['.jpg', '.png', '.bmp']:
            #imgpath = r"../../img/ruancai/"+file_name
            imgpath =imagepath+ file_name
            img_t = transform(Image.open(imgpath))
            if(torch.cuda.is_available()):#判断torch是否支持gpu
                batch_t = torch.unsqueeze(img_t, 0).cuda()
            else:
                batch_t = torch.unsqueeze(img_t, 0)
            out = model(batch_t)
            _, indices = torch.sort(out, descending=True)
            percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
            for idx in indices[0][:1]:#选择前5概率高的类别indices[0][:5]
                frameid=file_name[5:-4]
                framelist.append([frameid,(classes[idx], percentage[idx].item())[0]])
    #输出物体元素的计数结果从大到小排序
    # arr=Counter(list)
    # # 转化成列表
    # k = arr.most_common(len(arr))  # 找出全部元素从大到小的元素对应的次数
    # print(k)
    print(framelist)
    objectDetectionCsv(framelist,imagepath+"objection.csv")
    return framelist

def objectDetectionCsv(framelist, savePath):
    # path为输出路径和文件名，newline=''是为了不出现空行
    csvFile = open(savePath, "w+", newline='')
    # name为列名
    name = ['FrameId','Top1-Objects']
    try:
        writer = csv.writer(csvFile)
        writer.writerow(name)
        datarow=[]
        for i in range(len(framelist)):
            datarow=[framelist[i][0]]
            datarow.append(framelist[i][1])
            writer.writerow(datarow)
    finally:
        csvFile.close()

    tf = wordfrequency(savePath)
    plotwordcloud(tf)


# imagepath=r"../../img/ruancai/"
# objectDetection(imagepath)