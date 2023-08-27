import os
import easyocr
import cv2
import csv
from src.algorithms.wordcloud2frame import wordfrequencyStr,plotwordcloud

def getsubtitleEasyOcr(filepath):
    path=filepath
    print(path)
    cap = cv2.VideoCapture(path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(frame_count)
    #i=1
    subtitleList = []
    subtitleStr = ""
    i = 0
    _, frame = cap.read(i)
    img1=frame[630:680, 50:1000]
    i=i+1
    th=0.45
    reader = easyocr.Reader(['ch_sim', 'en'])    #EasyOcr
    while i<frame_count:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        _, frame = cap.read(i)
        img2=frame[630:680, 50:1000]
        subtitle_event=subtitleDetect(img1,img2,th)
        #print(i)
        if subtitle_event:
            print("FrameID",i)
            wordslist = reader.readtext(img2)
            print(wordslist)
            for w in wordslist:
                print(w)
                print(w[1])
                if w[1] is not None:
                    subtitleList.append([i,w[1]])
                    print(subtitleList)
                    subtitleStr=subtitleStr+w[1]
                    print(subtitleStr)
        else:
            img1=img2
        i = i + 48

        # if cv2.waitKey(10) & 0xff == ord("q"):
        #     break
    cap.release()
    print(subtitleList)
    print(subtitleStr)

    #subtitleStr="没有共产党就没有新中国"
    tf = wordfrequencyStr(subtitleStr)
    plotwordcloud(tf)

    return subtitleStr,subtitleList


def subtitle2Csv(subtitleList, savePath):
    # path为输出路径和文件名，newline=''是为了不出现空行
    if os.path.exists(savePath):
        os.remove(savePath)
    csvFile = open(savePath, "w+", newline='')
    # name为列名
    name = ['FrameId','Subtitles']
    try:
        writer = csv.writer(csvFile)
        writer.writerow(name)
        datarow=[]
        for i in range(len(subtitleList)):
            datarow=[subtitleList[i][0]]
            datarow.append(subtitleList[i][1])
            writer.writerow(datarow)
    finally:
        csvFile.close()

def subtitle2Srt(subtitleList, savePath):
    # path为输出路径和文件名，newline=''是为了不出现空行
    if os.path.exists(savePath):
        os.remove(savePath)
    with open(savePath, 'w') as f:
        for i in range(len(subtitleList)):
            f.write(str(i)+'\n')
            f.write(frames_to_timecode(25,subtitleList[i][0])+'--->'+frames_to_timecode(25,subtitleList[i][0]+25)+'\n')
            f.write(subtitleList[i][1]+'\n\n\n')
    print("subtitle2Srt is completed!")


def frames_to_timecode(framerate,frames):
    """
    FrameID to time format
    :param framerate: FPS
    :param frames: frameId
    :return: 00:00:01:01
    """
    return '{0:02d}:{1:02d}:{2:02d}:{3:02d}'.format(int(frames / (3600 * framerate)),
                                                    int(frames / (60 * framerate) % 60),
                                                    int(frames / framerate % 60),
                                                    int(frames % framerate))

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

def subtitleDetect(img1, img2, th):
    hash1 = aHash(img1)
    hash2 = aHash(img2)
    n = cmpHash(hash1, hash2)  # 不同加1，相同为0
    if n > th:
        subtitle_event=True
    else:
        subtitle_event=False
    return subtitle_event

def aHash(img):

    imgsmall = cv2.resize(img, (16, 4))
    # 转换为灰度图
    gray = cv2.cvtColor(imgsmall, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(4):
        for j in range(16):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 64
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(4):
        for j in range(16):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str

# path = "../../video/20210701.mp4"
# savepath=r'../../img/20210701/subtitle.srt'
# _,subtitleList=getsubtitleEasyOcr(path)
# # subtitle2Csv(subtitleList,savepath)
# subtitle2Srt(subtitleList,savepath)
# #print(frames_to_timecode(25,123))