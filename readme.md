PyCinemetrics, also known as CCKS-Cinemetrics (Chinese Cinema Knowledge System-Cinemetrics, (https://movie.yingshinet.com)), is a computational film studies tool.

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
