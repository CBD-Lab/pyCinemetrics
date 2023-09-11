import os
import cv2
import csv
import matplotlib.pyplot as plt

class resultsave:
    def __init__(self, image_save_path):
        self.image_save_path = image_save_path

    # 其他方法保持不变...

    def diff_csv(self, diff, shot_len):
        shotcut_csv = open(os.path.join(self.image_save_path, "shotcut.csv"), "w+", newline='')
        shotlen_csv = open(os.path.join(self.image_save_path, "shotlen.csv"), "w+", newline='')
        name1 = ['Id', 'frameDiff']
        name2 = ['start', 'end', 'length']

        if diff != 0:
            try:
                writer = csv.writer(shotcut_csv)
                writer.writerow(name1)
                for i in range(len(diff)):
                    writer.writerow([i, diff[i]])
            finally:
                shotcut_csv.close()

        try:
            writer = csv.writer(shotlen_csv)
            writer.writerow(name2)
            for i in range(len(shot_len)):
                writer.writerow(shot_len[i])
        finally:
            shotlen_csv.close()

    def plot_transnet_shotcut(self, shot_len):
        shot_id = [i for i in range(len(shot_len))]
        shot_length = [shot_len[i][2] for i in range(len(shot_len))]
        plt.clf()
        # 创建一个黑底的图形
        plt.figure(figsize=(8, 6))
        plt.style.use('dark_background')
        plt.bar(shot_id, shot_length, color='blue')
        plt.title('shot length',color="white")
        plt.savefig(os.path.join(self.image_save_path, 'shotlen.png'))

    def color_csv(self, colors):
        csv_file = open(os.path.join(self.image_save_path, "colors.csv"), "w+", newline='')
        name = ['FrameId']
        for i in range(15):
            name.append("Color" + str(i))

        try:
            writer = csv.writer(csv_file)
            writer.writerow(name)
            for i in range(len(colors)):
                datarow = [colors[i][0][5:-4]]
                for j in range(15):
                    datarow.append(colors[i][1][j])
                writer.writerow(datarow)
        finally:
            csv_file.close()

    def plot_scatter_3d(self, all_colors):
        plt.clf()
        plt.style.use('dark_background')
        movie_colors = []

        for i in all_colors:
            i = list(i)
            for j in i:
                movie_colors.append(list(j))

        x = []
        y = []
        z = []
        dot_color = []

        for c in movie_colors:
            x.append(c[0])
            y.append(c[1])
            z.append(c[2])
            dot_color.append([c[0] / 255, c[1] / 255, c[2] / 255, 1])

        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.scatter(x, y, z, c=dot_color, facecolor='black', edgecolor='black')
        fig.canvas.manager.set_window_title('imgcolors')
        plt.title("color analysis")
        plt.savefig(os.path.join(self.image_save_path, 'colors.png'))
        # plt.show()
