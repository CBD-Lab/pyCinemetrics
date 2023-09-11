import csv

import cv2
import time
import math
import numpy as np
from matplotlib import pyplot as plt
from collections import Counter

from src.algorithms.shotscaleconfig import *

class shotscale(object):

    # 初始化 Pose keypoint_num: 25 or 18
    def __init__(self, keypoint_num):
        self.point_names = point_name_25 if keypoint_num == 25 else point_names_18
        self.point_pairs = point_pairs_25 if keypoint_num == 25 else point_pairs_18
        self.map_idx = map_idx_25 if keypoint_num == 25 else map_idx_18
        self.colors = colors_25 if keypoint_num == 25 else colors_18
        self.num_points = 25 if keypoint_num == 25 else 18

        self.prototxt = prototxt_25 if keypoint_num == 25 else prototxt_18
        self.caffemodel = caffemodel_25 if keypoint_num == 25 else caffemodel_18
        self.pose_net = self.get_model()

    # 通过读取配置文件和权重文件，加载预训练的OpenPose模型
    def get_model(self):
        coco_net = cv2.dnn.readNetFromCaffe(self.prototxt, self.caffemodel)
        return coco_net

    # 预测（推理）关键点
    def predict(self, imgfile):
        img = cv2.imread(imgfile)
        height, width, _ = img.shape
        net_height = 368
        net_width = int((net_height / height) * width)
        start = time.time()

        # 将图像转换为神经网络的输入格式blob
        in_blob = cv2.dnn.blobFromImage(
            img, 1.0 / 255, (net_width, net_height), (0, 0, 0), swapRB=False, crop=False)
        self.pose_net.setInput(in_blob)
        # 执行模型的前向传播，得到输出
        output = self.pose_net.forward()
        # print("output", output)
        # print("[INFO]Time Taken in Forward pass: {} ".format(time.time() - start))
        detected_keypoints = []
        points_table = []
        keypoints_list = np.zeros((0, 3))
        keypoint_id = 0
        threshold = 0.1
        # 迭代不同的身体部位
        for part in range(self.num_points):
            # 获取关键点的置信度图
            probMap = output[0, part, :, :]
            probMap = cv2.resize(probMap, (width, height))

            # 使用阈值对置信度图进行阈值化处理，获得可能的关键点位置
            keypoints = self.getKeypoints(probMap, threshold)
            # print("Keypoints - {} : {}".format(self.point_names[part], keypoints))
            keypoint_with_id = []
            for i in range(len(keypoints)):
                points_table.append(keypoints[i] + (keypoint_id,) + (self.point_names[part],))
                # 给每个关键点赋予一个唯一的ID
                keypoint_with_id.append(keypoints[i] + (keypoint_id,))
                # print("keypoint_with_id", keypoint_with_id)
                # 存储所有检测到的关键点的位置信息，每个关键点一行
                keypoints_list = np.vstack([keypoints_list, keypoints[i]])  # 用于生成完整的人体姿态关键点信息
                # print("keypoints_list", keypoints_list)
                keypoint_id += 1

            detected_keypoints.append(keypoint_with_id)  # 用于确定有效的关键点对

        # print("detected_keypoints", detected_keypoints)
        valid_paris, invalid_pairs = self.getValidPairs(output, detected_keypoints, width, height)
        # print("valid_paris", valid_paris)
        # print("invalid_pairs", invalid_pairs)
        # 使用有效关键点对，计算出完整的人体姿态关键点信息
        # personwiseKeypoints是一个二维数组，其中每一行表示一个人体姿态，每列对应一个关键点或得分
        # 每个行（每个姿态）中的前self.num_points列对应一个关键点的索引（如：鼻子、左肩、右肩等），值表示相应关键点的检测到的关键点的ID
        # 每行中的最后一列表示该姿态的累积得分，由连接的关键点的概率和连接得分的累积组成，这个得分可以用来度量人体姿态的置信度
        personwiseKeypoints = self.getPersonwiseKeypoints(valid_paris, invalid_pairs, keypoints_list)
        # print("personwiseKeypoints", personwiseKeypoints)
        img = self.vis_pose(imgfile, personwiseKeypoints, keypoints_list)
        FPS = math.ceil(1 / (time.time() - start))

        key_parts, min_y, max_y = self.detect_key_person(personwiseKeypoints, points_table)
        type = self.shotsize(key_parts, min_y, max_y, height)
        img = cv2.putText(img, "FPS:" + str(int(FPS)), (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        img = cv2.putText(img, "ShotSize:" + str(type), (25, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        return img, type, len(personwiseKeypoints)

    # 通过阈值筛选出概率图中的有效关键点
    def getKeypoints(self, probMap, threshold=0.1):
        mapSmooth = cv2.GaussianBlur(probMap, (3, 3), 0, 0)
        mapMask = np.uint8(mapSmooth > threshold)
        keypoints = []

        # 找到关键点的连通区域，每个区域中概率最大的位置作为关键点位置
        contours, hierarchy = cv2.findContours(mapMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            blobMask = np.zeros(mapMask.shape)
            blobMask = cv2.fillConvexPoly(blobMask, cnt, 1)
            maskedProbMap = mapSmooth * blobMask
            _, maxVal, _, maxLoc = cv2.minMaxLoc(maskedProbMap)
            keypoints.append(maxLoc + (probMap[maxLoc[1], maxLoc[0]],))
        return keypoints

    # 根据模型输出的概率图和关键点信息，计算出有效的关键点对以及无效的关键点对，用于绘制骨骼图
    def getValidPairs(self, output, detected_keypoints, width, height):
        valid_pairs = []
        invalid_pairs = []
        n_interp_samples = 15  # 插值样本数
        paf_score_th = 0.1  # 分数阈值
        conf_th = 0.7  # 置信度阈值

        for k in range(len(self.map_idx)):
            # A -> B 构成身体部位的连接
            pafA = output[0, self.map_idx[k][0], :, :]
            pafB = output[0, self.map_idx[k][1], :, :]
            pafA = cv2.resize(pafA, (width, height))
            pafB = cv2.resize(pafB, (width, height))

            candA = detected_keypoints[self.point_pairs[k][0]]
            candB = detected_keypoints[self.point_pairs[k][1]]
            # print("candA", candA)
            # print("candB", candB)
            nA = len(candA)
            nB = len(candB)
            if (nA != 0 and nB != 0):
                valid_pair = np.zeros((0, 3))
                for i in range(nA):
                    max_j = -1
                    maxScore = -1
                    found = 0
                    for j in range(nB):
                        # 计算从部位A的关键点到部位B的关键点的位移向量
                        d_ij = np.subtract(candB[j][:2], candA[i][:2])
                        # 计算范数，得到连接的长度
                        norm = np.linalg.norm(d_ij)
                        if norm:
                            d_ij = d_ij / norm  # 归一化
                        else:
                            continue
                        # 使用线性插值，生成插值坐标
                        interp_coord = list(
                            zip(np.linspace(candA[i][0], candB[j][0], num=n_interp_samples),
                                np.linspace(candA[i][1], candB[j][1], num=n_interp_samples)))
                        # 提取插值得到的PAF分数
                        paf_interp = []
                        for k in range(len(interp_coord)):
                            paf_interp.append([pafA[int(round(interp_coord[k][1])), int(round(interp_coord[k][0]))],
                                               pafB[int(round(interp_coord[k][1])), int(round(interp_coord[k][0]))]])
                        # 计算插值得到的PAF分数与连接方向向量的点积，得到一个分数数组
                        paf_scores = np.dot(paf_interp, d_ij)
                        # 计算插值坐标上的平均 PAF 分数
                        avg_paf_score = sum(paf_scores) / len(paf_scores)
                        # 判断连接的有效性
                        # 如果与PAF对齐的插值向量的比例高于阈值 -> 有效点对
                        if (len(np.where(paf_scores > paf_score_th)[0]) / n_interp_samples) > conf_th:
                            if avg_paf_score > maxScore:
                                max_j = j
                                maxScore = avg_paf_score
                                found = 1
                    # Append the connection to the list
                    if found:
                        valid_pair = np.append(valid_pair, [[candA[i][3], candB[max_j][3], maxScore]], axis=0)

                # Append the detected connections to the global list
                valid_pairs.append(valid_pair)

            else:  # If no keypoints are detected
                # print("No Connection : k = {}".format(k))
                invalid_pairs.append(k)
                valid_pairs.append([])

        return valid_pairs, invalid_pairs

    # 连接有效点对，获取完整的人体骨骼图
    def getPersonwiseKeypoints(self, valid_pairs, invalid_pairs, keypoints_list):
        personwiseKeypoints = -1 * np.ones((0, self.num_points + 1))
        for k in range(len(self.map_idx)):
            if k not in invalid_pairs:
                # 从有效连接列表中获取关键点连接的部位A和部位B的索引
                partAs = valid_pairs[k][:, 0]
                partBs = valid_pairs[k][:, 1]
                # print("partAs", partAs)
                # print("partBs", partBs)
                indexA, indexB = np.array(self.point_pairs[k])
                # print("indexA", indexA)
                # print("indexB", indexB)
                for i in range(len(valid_pairs[k])):
                    found = 0
                    person_idx = -1
                    for j in range(len(personwiseKeypoints)):
                        if personwiseKeypoints[j][indexA] == partAs[i]:
                            person_idx = j
                            found = 1
                            break
                    if found:
                        personwiseKeypoints[person_idx][indexB] = partBs[i]
                        personwiseKeypoints[person_idx][-1] += keypoints_list[partBs[i].astype(int), 2] + \
                                                               valid_pairs[k][i][2]
                    elif not found and k < self.num_points - 1:
                        row = -1 * np.ones(self.num_points + 1)
                        row[indexA] = partAs[i]
                        row[indexB] = partBs[i]
                        row[-1] = sum(keypoints_list[valid_pairs[k][i, :2].astype(int), 2]) + \
                                  valid_pairs[k][i][2]
                        personwiseKeypoints = np.vstack([personwiseKeypoints, row])
        return personwiseKeypoints

    # 关键点连接后的可视化
    def vis_pose(self, img_file, personwiseKeypoints, keypoints_list):
        img = cv2.imread(img_file)
        for i in range(self.num_points - 1):
            for n in range(len(personwiseKeypoints)):
                index = personwiseKeypoints[n][np.array(self.point_pairs[i])]
                if -1 in index:
                    continue
                B = np.int32(keypoints_list[index.astype(int), 0])
                A = np.int32(keypoints_list[index.astype(int), 1])
                # print("B", B)
                # print("A", A)
                cv2.line(img, (B[0], A[0]), (B[1], A[1]), self.colors[i], 3, cv2.LINE_AA)
        # img = cv2.resize(img, (480, 640))
        return img

    # 获取面积占比最大的关键人物
    def detect_key_person(self, personwiseKeypoints, points_table):
        max_area = 0
        key_person_index = -1
        key_parts = []
        min_y = 0
        max_y = 0

        for i, person_keypoints in enumerate(personwiseKeypoints):
            x_coordinates = []
            y_coordinates = []
            part = []
            # print("i", i)
            # print("person_keypoints", person_keypoints)
            for j in range(self.num_points):
                value = np.int32(person_keypoints[j])
                if value != -1:
                    for points in points_table:
                        if points[3] == value:
                            x_coordinates.append(points[0])
                            y_coordinates.append(points[1])
                            part.append(points[4])
            # print("x_coordinates", x_coordinates)
            # print("y_coordinates", y_coordinates)
            # print("part", part)

            min_x = np.min(x_coordinates)
            max_x = np.max(x_coordinates)
            min_y = np.min(y_coordinates)
            max_y = np.max(y_coordinates)
            area = (max_x - min_x) * (max_y - min_y)

            if area > max_area:
                max_area = area
                key_person_index = i
                key_parts = part

        if key_person_index != -1:
            keyperson_keypoints = personwiseKeypoints[key_person_index]
            return key_parts, min_y, max_y
        else:
            return None, None, None

    # 景别分类
    def shotsize(self, key_parts, min_y, max_y, height):
        if key_parts is None:
            return "Empty Shot"  # 空景
        else:
            body_parts = set(key_parts)
            head_parts = {'Nose', 'REye', 'LEye', 'REar', 'LEar'}
            chest_below_parts = {'MidHip', 'RHip', 'LHip', 'RKnee', 'LKnee'}
            feet_parts = {'RAnkle', 'LAnkle', 'RHeel', 'LHeel', 'RBigToe', 'LBigToe', 'RSmallToe', 'LSmallToe'}
            if body_parts.intersection(head_parts) and body_parts.intersection(feet_parts):
                if (max_y - min_y) <= height / 2:
                    return "Long Shot"  # 远景
                else:
                    return "Full Shot"  # 全景
            elif body_parts.intersection(head_parts) and not body_parts.intersection(feet_parts) \
                    and body_parts.intersection(chest_below_parts):
                return "Medium Shot"  # 中景
            elif body_parts.intersection(head_parts) and not body_parts.intersection(chest_below_parts) \
                    and body_parts.issuperset({'Neck'}):
                return "Medium Close-Up"  # 近景
            elif body_parts.intersection(head_parts) and not body_parts.issuperset({'Neck'}):
                return "Close-Up"  # 特写
            else:
                return "Close-Up"  # 身体特写

    def shotscale_csv(self, detectInfo, savePath):
        # path为输出路径和文件名，newline=''是为了不出现空行
        shotscale_csv = open(savePath + "/shotscale.csv", "w+", newline='')
        # name为列名
        name = ['FrameId', 'ShotScale', 'Detect_Person_Num']
        try:
            writer = csv.writer(shotscale_csv)
            writer.writerow(name)
            # data为list类型
            for i in range(len(detectInfo)):
                writer.writerow([detectInfo[i][0], detectInfo[i][1], detectInfo[i][2]])
        finally:
            shotscale_csv.close()

    def shotscale_plot(self, detectInfo, image_save):

        # 饼图
        categories = [item[1] for item in detectInfo]
        category_counts = Counter(categories)
        sizes = [(count / len(categories)) * 100 for count in category_counts.values()]
        labels = list(category_counts.keys())

        inner_radius = 0.5
        width = 0.3
        plt.clf()
        plt.style.use('dark_background')
        plt.pie(sizes, labels=labels, autopct='%0.1f%%', shadow=True, pctdistance=0.5,
                wedgeprops=dict(width=width, edgecolor='w'))
        centre_circle = plt.Circle((0, 0), inner_radius, fc='black')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.title('Shot Scale')
        plt.axis('equal')
        plt.savefig(image_save + '/shotscale.png')
        # plt.show()