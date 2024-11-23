PyCinemetrics, also known as CCKS-Cinemetrics (Chinese Cinema Knowledge System-Cinemetrics, (https://movie.yingshinet.com)), is a computational film studies tool.
## Paper Links
https://www.sciencedirect.com/science/article/pii/S2352711024000578
https://movie.yingshinet.com/#/video?id=254
## Daoxin Li‘s comments
https://mp.weixin.qq.com/s/xDrzASlrZDRStq45nPKf_Q
## 中文简介
功能包括：分镜、色彩提取、物体识别、字幕识别、景别识别。
 CCKS-Cinemetrics（别名PyCinemetrics）是国内第一款专用的计量电影研究工具，提供了五个功能，利用深度学习和PySide2 来解构电影的视觉风格。它使用 TransNetV2 将电影分割成镜头帧，探索平均镜头长度（Average Shot Length）和节奏。利用 K-Means 从镜头帧中提取主要颜色。使用 EasyOcr 提取电影字幕以获取影片对白。基于 VGG19 的目标检测来识别隐喻性道具和物体。通过 OpenPose 检测骨骼点的比例以及在画面的占比，间接确定拍摄景别。基于PySide2 集成PyCinemetrics 的各个功能并提供良好的扩展性，如替换智能模块。使用CCKS-Cinemetrics 对一组经典电影进行了计量分析，实验验证了在帧分析中的准确性和效率。
## 下载
# 2024年4月20日版本（仅Windows系统）。QQ:115305288/微信：leerose2015
# --------CCKS-Cinemetrics软件下载-----------
# 链接：https://pan.baidu.com/s/1U4mtpz8obn6VnsvreazW8g?pwd=2024 提取码：2024

## What does the project do?
PyCinemetrics is a powerful software tool for film analysis that utilizes deep learning and PySide2 to deconstruct the visual style of films. It employs TransNetV2 to divide a film into shot-frames, enabling the exploration of Average Shot Length (ASL) and pace. The tool also extracts main colors from shot-frames using K-Means. It can extract movie subtitles using EasyOcr for dialogue analysis. Additionally, PyCinemetrics utilizes object detection based on VGG19 to identify metaphorical props and objects. By detecting the proportion of skeletal points occupied in the frame using OpenPose, it indirectly determines the shot scale. Finally, PyCinemetrics is integrated and implemented using PySide2.

## Why is the project useful?
PyCinemetrics is specifically designed for film analysis and stands out from previous software tools by integrating various pre-trained deep learning algorithms such as shot segmentation, subtitle recognition, object recognition, and pose estimation. Unlike manual shot boundary detection, PyCinemetrics combines these AI algorithms using PySide2 to create a comprehensive tool for film measurement analysis. It provides shot-frames as a storyboard, visual charts, and data files (.csv and .srt) for further analysis.

## How can users get started with the project?
To get started with PyCinemetrics, simply download the source code from [https://github.com/CBD-Lab/pyCinemetrics](https://github.com/CBD-Lab/pyCinemetrics).

## Where can users get help with the project?
For any assistance or inquiries regarding the project, please reach out via email to 115305288@qq.com(Chunfang Li) or visit [https://movie.yingshinet.com](https://movie.yingshinet.com).

## Who maintains and contributes to the project?
PyCinemetrics is sponsored by Chunfang Li(Communication University of China), and the development of this software has been contributed to by Junli Lu, Yuchen Pei, Yuhang Hu, Yalv Fan, Yanzhi Tian, Xiaoyu Linghu, Kun Wang, and Jiangnan Sun.
Professor Daoxin Li(Peking University) serves as the advisor for this technology project in the field of digital humanities and film studies.
