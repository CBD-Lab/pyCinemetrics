import jieba
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import csv


def wordfrequency(filename):
    #data = np.loadtxt(open(csvfile, "rb"),  skiprows=1, usecols=[1, 1])
    print(filename)
    data = []
    with open(filename) as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        # header = next(csv_reader)        # 读取第一行每一列的标题
        for row in csv_reader:  # 将csv 文件中的数据保存到data中
            data.append(row[1])  # 选择某一列加入到data数组中
        print(data)


    #jieba.load_userdict(r'./src/algorithms/AIDict.txt')
    print(data)
    allstr=""
    for d in data:
        allstr=allstr+d
    print(allstr)
    seg_list = jieba.cut(allstr, cut_all=False)

    tf = {}
    for seg in seg_list:
        if seg in tf:
            tf[seg] += 1
        else:
            tf[seg] = 1
    ci = list(tf.keys())
    # with open('stopword.txt', 'r') as ft:
    #     stopword = ft.read()

    for seg in ci:
        if tf[seg] < 1 or len(seg) < 0 or "一" in seg  or " " in seg  or ";" in seg or "-" in seg:  #or seg in stopword
            tf.pop(seg)

    print(tf)

    ci, num, data = list(tf.keys()), list(tf.values()), []
    for i in range(len(tf)):
        data.append((num[i], ci[i]))  # 逐个将键值对存入data中
    data.sort()  # 升序排列
    data.reverse()  # 逆序，得到所需的降序排列

    tf_sorted = {}
    print(len(data), data[0], data[0][0], data[0][1])

    for i in range(len(data)):
        tf_sorted[data[i][1]] = data[i][0]
    print(tf_sorted)
    return tf_sorted

def wordfrequencyStr(datastr):
    seg_list = jieba.cut(datastr, cut_all=False)
    tf = {}
    for seg in seg_list:
        if seg in tf:
            tf[seg] += 1
        else:
            tf[seg] = 1
    ci = list(tf.keys())
    # with open('stopword.txt', 'r') as ft:
    #     stopword = ft.read()

    for seg in ci:
        if tf[seg] < 1 or len(seg) < 0 or "一" in seg  or " " in seg  or ";" in seg or "-" in seg:  #or seg in stopword
            tf.pop(seg)

    print(tf)

    ci, num, data = list(tf.keys()), list(tf.values()), []
    for i in range(len(tf)):
        data.append((num[i], ci[i]))  # 逐个将键值对存入data中
    data.sort()  # 升序排列
    data.reverse()  # 逆序，得到所需的降序排列

    tf_sorted = {}
    print(len(data), data[0], data[0][0], data[0][1])

    for i in range(len(data)):
        tf_sorted[data[i][1]] = data[i][0]
    print(tf_sorted)
    return tf_sorted


def plotwordcloud(tf_sorted):
    font=r'c:\Windows\Fonts\simfang.ttf'
    print(tf_sorted)
    wc=WordCloud(font_path=font,width=800,height=600).generate_from_frequencies(tf_sorted)
    plt.axes(facecolor='black')
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    wc.to_file('objects.png')

# csvfile=r'..\..\img\ruancai\objection.csv'
# tf=wordfrequency(csvfile)
# plotwordcloud(tf)

