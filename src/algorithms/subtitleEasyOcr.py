import os
import re

import easyocr
import cv2
import csv
from src.algorithms.wordcloud2frame import WordCloud2Frame

class SubtitleProcessor:
    def __init__(self):
        self.reader = easyocr.Reader(['ch_sim', 'en'])
    def getsubtitleEasyOcr(self,v_path,save_path,subtitleValue):
        path=v_path
        cap = cv2.VideoCapture(path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        subtitleList = []
        subtitleStr = ""
        i = 0
        _, frame = cap.read(i)
        h,w=frame.shape[0:2]#图片尺寸，截取下三分之一和中间五分之四作为字幕检测区域
        start_h = (h // 3)*2
        end_h = h
        start_w = w // 20
        end_w = (w // 20) * 19
        img1=frame[start_h:end_h,start_w:end_w,:]
        i=i+1
        th=0.2
        while i<frame_count:
            if img1 is None:
                break
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            _, frame = cap.read(i)
            h, w = frame.shape[0:2]  # 图片尺寸，截取下五分之一和中间五分之四作为字幕检测区域
            start_h = (h // 5)*4
            end_h = h
            start_w = w // 10
            end_w = (w // 10) * 9
            img2 = frame[start_h:end_h, start_w:end_w]
            subtitle_event= self.subtitleDetect(img1, img2, th)
            if subtitle_event:
                wordslist = self.reader.readtext(img2)
                # print("wordlist",wordslist)
                # subtitleStr=subtitleStr+
                for w in wordslist:
                    # print('w',w,w[1])
                    if w[1] is not None:
                        print("w1",w[1])
                        if (not subtitleList or w[1]+'\n' != subtitleList[-1][1]) and (not self.contains_english(w[1])):
                            subtitleList.append([i,w[1]])
                            subtitleStr=subtitleStr+w[1]+'\n'
            else:
                img1=img2
            i = i + subtitleValue
            #12-120，默认48帧
        cap.release()
        wc2f=WordCloud2Frame()
        tf = wc2f.wordfrequencyStr(subtitleStr)
        wc2f.plotwordcloud(tf,save_path,"subtitle")

        return subtitleStr,subtitleList

    def subtitle2Srt(self,subtitleList, savePath):
        # path为输出路径和文件名，newline=''是为了不出现空行
        csvpath=savePath+"subtitle.csv"
        csvFile = open(csvpath, "w+", newline='')
        srtFile=savePath+"subtitle.srt"
        # name为列名
        name = ['FrameId','Subtitles']
        try:
            writer = csv.writer(csvFile)
            writer.writerow(name)
            for i in range(len(subtitleList)):
                datarow=[subtitleList[i][0]]
                datarow.append(subtitleList[i][1])
                writer.writerow(datarow)
        finally:
            csvFile.close()
        with open(srtFile, 'w', encoding='utf-8') as f:
            for i in range(len(subtitleList)):
                f.write(str(subtitleList[i][1])+'\n')
    #
    # def subtitle2Csv(subtitleList, savePath):
    #     # path为输出路径和文件名，newline=''是为了不出现空行
    #     if os.path.exists(savePath):
    #         os.remove(savePath)
    #     csvFile = open(savePath, "w+", newline='')
    #     # name为列名
    #     name = ['FrameId','Subtitles']
    #     try:
    #         writer = csv.writer(csvFile)
    #         writer.writerow(name)
    #         datarow=[]
    #         for i in range(len(subtitleList)):
    #             datarow=[subtitleList[i][0]]
    #             datarow.append(subtitleList[i][1])
    #             writer.writerow(datarow)
    #     finally:
    #         csvFile.close()

    # def subtitle2Srt(subtitleList, savePath):
    #     # path为输出路径和文件名，newline=''是为了不出现空行
    #     print(savePath)
    #     try:
    #         if os.path.exists(savePath):
    #             os.remove(savePath)
    #     except PermissionError as e:
    #         print("删除文件失败，权限错误:", e)
    #
    #     with open(savePath, 'w') as f:
    #         for i in range(len(subtitleList)):
    #             f.write(str(i)+'\n')
    #             f.write(frames_to_timecode(25,subtitleList[i][0])+'--->'+frames_to_timecode(25,subtitleList[i][0]+25)+'\n')
    #             f.write(subtitleList[i][1]+'\n\n\n')
    #     print("subtitle2Srt is completed!")


    # def frames_to_timecode(framerate,frames):
    #     """
    #     FrameID to time format
    #     :param framerate: FPS
    #     :param frames: frameId
    #     :return: 00:00:01:01
    #     """
    #     return '{0:02d}:{1:02d}:{2:02d}:{3:02d}'.format(int(frames / (3600 * framerate)),
    #                                                     int(frames / (60 * framerate) % 60),
    #                                                     int(frames / framerate % 60),
    #                                                     int(frames % framerate))
    #根据阈值判断是否再次提取图片字幕
    def cmpHash(self,hash1, hash2):
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

    def aHash(self, img):
        if img is None:
            print("none")
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
        # 遍历图像的每个像素，并比较每个像素的灰度值是否大于平均灰度值 avg。如果大于 avg，则将 '1' 添加到 hash_str 中，否则添加 '0'。这样就生成了一个二进制的哈希字符串
        for i in range(4):
            for j in range(16):
                if gray[i, j] > avg:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'
        return hash_str

    def subtitleDetect(self,img1, img2, th):
        hash1 = self.aHash(img1)
        hash2 = self.aHash(img2)
        n = self.cmpHash(hash1, hash2)  # 不同加1，相同为0
        if n > th:
            subtitle_event=True
        else:
            subtitle_event=False
        return subtitle_event

    def contains_english(self,text):
        # 使用正则表达式匹配英文字符
        english_pattern = re.compile(r'[a-zA-Z]')
        return bool(english_pattern.search(text))

