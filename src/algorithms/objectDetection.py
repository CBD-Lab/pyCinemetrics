import os
import numpy as np
from collections import Counter

from PIL import Image
import csv
import torch
import torch.nn
import torchvision.models as models
import torch.cuda
from torchvision import transforms
from .wordcloud2frame import WordCloud2Frame


class ObjectDetection:
    def __init__(self, image_path):
        self.image_path = image_path
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )])

    def make_model(self):
        model = models.vgg19(pretrained=True)
        model = model.eval()
        if torch.cuda.is_available():
            model.cuda()
        return model

    def object_detection(self):
        model = self.make_model()
        if self.image_path is None or self.image_path == '':
            return

        file_list = os.listdir(self.image_path+"/frame/")
        framelist = []

        with open('./src/algorithms/imagenet_classes.txt') as f:
            classes = [line.strip() for line in f.readlines()]

        for file_name in file_list:
            if os.path.splitext(file_name)[-1] in ['.jpg', '.png', '.bmp']:
                img_path = self.image_path+"/frame/"+file_name
                img_t = self.transform(Image.open(img_path))

                if torch.cuda.is_available():
                    batch_t = torch.unsqueeze(img_t, 0).cuda()
                else:
                    batch_t = torch.unsqueeze(img_t, 0)

                out = model(batch_t)
                _, indices = torch.sort(out, descending=True)
                percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

                for idx in indices[0][:1]:
                    frame_id = file_name[5:-4]
                    framelist.append([frame_id, (classes[idx], percentage[idx].item())[0]])

        self.object_detection_csv(framelist, self.image_path)

    def object_detection_csv(self, framelist, save_path):
        csv_file = open(os.path.join(save_path, 'objects.csv'), "w+", newline='')
        name = ['FrameId', 'Top1-Objects']

        try:
            writer = csv.writer(csv_file)
            writer.writerow(name)
            datarow = []

            for i in range(len(framelist)):
                datarow = [framelist[i][0]]
                datarow.append(framelist[i][1])
                writer.writerow(datarow)
        finally:
            csv_file.close()

        wc2f = WordCloud2Frame()
        tf = wc2f.wordfrequency(os.path.join(save_path, 'objects.csv'))
        wc2f.plotwordcloud(tf, save_path, "/objects")
