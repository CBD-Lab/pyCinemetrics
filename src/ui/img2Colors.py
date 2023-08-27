from PIL import Image
import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten
import matplotlib.pyplot as plt
import os

def colordata(filename):
    img=Image.open(filename)
    #print(filename)
    #print(img)
    img=img.rotate(-90)
    img.thumbnail((200,200))
    w,h=img.size
    points=[]
    for count,color in img.getcolors(w*h):
        points.append(color)
    return points

# print(os.getcwd())
# colordata("../static/spring.jpg")



def kmeansFun(data, n):
    data = np.array(data, dtype=float)  # 聚类需要是Float或者Double
    center_init = np.array(data[0:n])  # 初始聚类中心
    # print(type(center_init))
    #
    # print(type(center_init))
    # print("Center_init: \n", center_init)

    centers, loss = kmeans(data, n)  # n是聚类中心个数
    # 可以写kmeans(wf,2)， 2表示两个质心，同时启用iter参数

    # print("Loss: ", loss)
    centers=np.array(centers,dtype=int)
    #print("Centers:\n", centers)
    return centers

# imgdata = colordata("../img/20210701/image0.png")
# kmeansFun(imgdata, 5)

