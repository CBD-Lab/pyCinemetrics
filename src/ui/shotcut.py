import cv2
import csv
from .img2Colors import *


# Hash值对比

import matplotlib.pyplot as plt

def cmpHash(hash1, hash2):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        if hash1[i] != hash2[i]:
            n = n + 1
    n = n/len(hash1)
    return n


def findshot(v_path, image_save, th):
    # 删除旧的分镜
    print(image_save)
    if not (os.path.exists(image_save)):
        os.mkdir(image_save)
    else:
        imgfiles=os.listdir(os.getcwd()+"/"+image_save)
        for f in imgfiles:
            os.remove(os.getcwd()+"/"+image_save+"/"+f)
    cap = cv2.VideoCapture(v_path)
    print(cap)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(frame_count)
    frame_len = len(str((int)(frame_count)))

    i = 0
    _, img1 = cap.read()
    frameid = ""
    for j in range(frame_len-len(str(i))):
        frameid = frameid+"0"
    cv2.imwrite(image_save+"/image"+frameid+str(i)+".png", img1)
    diff = []
    for i in range(1, int(frame_count-1)):
        _, img2 = cap.read()
        hash1 = aHash(img1)
        hash2 = aHash(img2)
        n = cmpHash(hash1, hash2)  # 不同加1，相同为0
        diff.append(n)
        if n > th:
            frameid = ""
            for j in range(frame_len - len(str(i))):
                frameid = frameid + "0"
            cv2.imwrite(image_save + "/image" +
                        frameid + str(i) + ".png", img2)
            print(i, '均值哈希算法相似度：', n)
        img1 = img2
    print("ShotCut completed")
    plotDiff(diff, image_save)
    diffCsv(diff, image_save+".csv")


def aHash(img):

    img = cv2.resize(img, (8, 8))
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(8):
        for j in range(8):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 64
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(8):
        for j in range(8):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str

def plotDiff(diff, image_save):
    x = [i for i in range(len(diff))]
    plt.figure(facecolor='black', edgecolor='black')
    ax = plt.axes(facecolor='black')
    plt.plot(x, diff, color='blue')
    plt.savefig(image_save+".png")
    plt.show()


def diffCsv(diff, savePath):
    # path为输出路径和文件名，newline=''是为了不出现空行
    csvFile = open(savePath, "w+", newline='')
    # name为列名
    name = ['Id', 'frameDiff']
    try:
        writer = csv.writer(csvFile)
        writer.writerow(name)
        # data为list类型
        for i in range(len(diff)):
            writer.writerow([i, diff[i]])
    finally:
        csvFile.close()

def imgColors(imgpath,colorsC):
    imglist = os.listdir("img/" + imgpath)
    colorlist = []
    allcolors=[]
    #print(imglist)
    for i in imglist:
        # imgdata = colordata("../img/20210701/image0.png")
        imgdata = colordata("img/"+imgpath+"/"+i)
        colors = kmeansFun(imgdata, colorsC)   #提取几种色彩
        allcolors.append((list)(colors))#用于plot3D
        colorsNew=colors.reshape(1,3*colorsC)
        colorlist.append([i,colorsNew[0]])
    #print(colorlist)
    colorCsv(colorlist,"img/"+imgpath+"colors.csv")
    plotScatter3D(allcolors,"img/"+imgpath+"allcolors.png")


def colorCsv(colors, savePath):
    # path为输出路径和文件名，newline=''是为了不出现空行
    csvFile = open(savePath, "w+", newline='')
    # name为列名
    name = ['FrameId']
    for i in range(15):
        name.append("Color"+str(i))
    #print(name)
    try:
        writer = csv.writer(csvFile)
        writer.writerow(name)
        # data为list类型
        for i in range(len(colors)):
            datarow=[colors[i][0][5:-4]]
            for j in range(15):
                datarow.append(colors[i][1][j])
            writer.writerow(datarow)
    finally:
        csvFile.close()


def plotScatter3D(allcolors, image_save):
    #plt.style.use('_mpl-gallery')
    plt.style.use('dark_background')
    moviecolors=[]
    for i in allcolors:
        i=(list)(i)
        for j in i:
            moviecolors.append((list)(j))
    x=[]
    y=[]
    z=[]
    dotcolor=[]
    for c in moviecolors:
        x.append(c[0])
        y.append(c[1])
        z.append(c[2])
        dotcolor.append([c[0]/255,c[1]/255,c[2]/255,1])

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.scatter(x, y, z,c=dotcolor,facecolor='black', edgecolor='black')
    plt.show()
    plt.savefig(image_save)


# v_path='../video/20210701.mp4'
# image_save="../img/20210701"
# th=0.5
# findshot(v_path,image_save,th)
