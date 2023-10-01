PyCinemetrics is also named CCKS-Cinemetrics(Chinese Cinema Knowledge System-Cinemetrics, Https://movie.yingshinet.com).
1-What the project does
PyCinemetrics is a computational film studies tool that offers five functions using deep learning and PySide2 to deconstruct films visual style. It uses TransNetV2 to divide a film into shot-frames, allowing for the exploration of Average Shot Length (ASL) and pace. The tool also extracts main colors from shot-frames using K-Means . It can extract movie subtitles using EasyOcr to obtain dialogue. Additionally, PyCinemetrics utilizes object detection based on VGG19 to identify metaphorical props and objects. By detecting the proportion of skeletal points occupied in the frame using OpenPose, it indirectly determines the shot scale. Finally, PyCinemetrics was integrated and implemented using PySide2.
2-Why the project is useful
PyCinemetrics is a software specifically designed for film analysis, which
sets itself apart from previous software tools by integrating various pre-
trained deep learning algorithms such as shot segmentation, subtitle recog-
nition, object recognition, and pose estimation. Unlike the manual shot
boundary detection of Cinemetrics, PyCinemetrics combines these AI algo-
rithms using PySide2 to create a comprehensive tool for film measurement
analysis. It provides shot-frames as a storyboard, some visual charts, and
several data files(.csv and .srt) for further analysis.
3-How users can get started with the project
Download the source code from https://github.com/CBD-Lab/pyCinemetrics.

4-Where users can get help with your project
Mail to: 115305288@qq.com
Https://movie.yingshinet.com
5-Who maintains and contributes to the project
It has sponsored by Chunfang Li, and Junli Lu, Yuchen Pei, Yuhang Hu, Yalv Fan, Yanzhi tian, Xiaoyu Linghu, Kun Wang, Jiangnan Sun have all made contributions to the development of this software.
