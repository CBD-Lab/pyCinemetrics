#! /usr/bin/env python3
#
# PySide2 example for VLC Python bindings
# Copyright (C) 2009-2010 the VideoLAN team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#
'''
A simple example for VLC python bindings using PySide2.

Author: Saveliy Yusufov, Columbia University, sy2685@columbia.edu
Date: 25 December 2018
'''

import sys
import platform
import time

from PySide2 import QtWidgets, QtGui, QtCore
import os
import vlc


class VLCPlayer(QtWidgets.QWidget):
    '''A simple Media Player using VLC and Qt
    '''

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

        # Create a basic vlc instance
        self.instance = vlc.Instance()

        self.media = None

        # Create an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.init_ui()
        self.is_paused = False
        self.total_time_label = QtWidgets.QLabel(self)
        self.total_time_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.total_time_label.setFixedWidth(55)
        self.total_time_label.setFixedHeight(20)

        self.current_time_label = QtWidgets.QLabel(self)
        self.current_time_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.current_time_label.setFixedWidth(55)
        self.current_time_label.setFixedHeight(20)
        self.hbuttonbox.addWidget(self.current_time_label)
        self.hbuttonbox.addWidget(QtWidgets.QLabel("/", self))
        self.hbuttonbox.addWidget(self.total_time_label)

    def init_ui(self):
        '''Set up the user interface, signals & slots
        '''

        # In this widget, the video will be drawn
        if platform.system() == 'Darwin':  # for MacOS
            self.videoframe = QtWidgets.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtWidgets.QFrame()

        self.icons = {
            'OPEN': self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon),
            'PLAY': self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay),
            'PAUSE': self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause),
            'STOP': self.style().standardIcon(QtWidgets.QStyle.SP_MediaStop)
        }

        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.positionslider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.positionslider.setToolTip('Position')
        self.positionslider.setMaximum(2000)
        self.positionslider.sliderMoved.connect(self.set_position)
        self.positionslider.sliderPressed.connect(self.set_position)

        self.hbuttonbox = QtWidgets.QHBoxLayout()
        self.openbutton = QtWidgets.QPushButton()
        self.openbutton.setIcon(self.icons['OPEN'])
        self.hbuttonbox.addWidget(self.openbutton)
        self.openbutton.clicked.connect(self.open_file)

        self.playbutton = QtWidgets.QPushButton()
        self.playbutton.setIcon(self.icons['PLAY'])
        self.hbuttonbox.addWidget(self.playbutton)
        self.playbutton.clicked.connect(self.play_pause)

        self.stopbutton = QtWidgets.QPushButton()
        self.stopbutton.setIcon(self.icons['STOP'])
        self.hbuttonbox.addWidget(self.stopbutton)
        self.stopbutton.clicked.connect(self.stop)
        self.hbuttonbox.addStretch(1)
        self.volumeslider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.setToolTip('Volume')
        self.hbuttonbox.addWidget(self.volumeslider)
        self.volumeslider.valueChanged.connect(self.set_volume)
        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addWidget(self.positionslider)

        self.vboxlayout.addLayout(self.hbuttonbox)
        self.setLayout(self.vboxlayout)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_ui)

    def play_pause(self):
        '''Toggle play/pause status
        '''
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setIcon(self.icons['PLAY'])
            self.is_paused = True
            self.timer.stop()
        else:
            if self.mediaplayer.play() == -1:
                self.open_file()
                return

            self.mediaplayer.play()
            self.playbutton.setIcon(self.icons['PAUSE'])
            self.timer.start()
            self.is_paused = False

    def stop(self):
        '''Stop player
        '''
        self.mediaplayer.stop()
        self.positionslider.setValue(0)
        self.playbutton.setIcon(self.icons['PLAY'])

    def open_file(self):
        '''Open a media file in a MediaPlayer
        '''

        dialog_txt = 'Choose Media File'
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self, dialog_txt, os.path.expanduser('~'))
        if not filename:
            return

        # getOpenFileName returns a tuple, so use only the actual file name
        self.media = self.instance.media_new(filename[0])

        # Put the media in the media player
        self.mediaplayer.set_media(self.media)

        # Parse the metadata of the file
        self.media.parse()

        # Set the title of the track as window title
        self.parent.filename_changed.emit(filename[0])

        # The media player has to be 'connected' to the QFrame (otherwise the
        # video would be displayed in it's own window). This is platform
        # specific, so we must give the ID of the QFrame (or similar object) to
        # vlc. Different platforms have different functions for this
        if platform.system() == 'Linux':  # for Linux using the X Server
            self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == 'Windows':  # for Windows
            self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == 'Darwin':  # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))

        time.sleep(0.2)
        self.play_pause()

    def set_volume(self, volume):
        '''Set the volume
        '''
        self.mediaplayer.audio_set_volume(volume)

    def set_position(self):
        '''Set the movie position according to the position slider.
        '''

        # The vlc MediaPlayer needs a float value between 0 and 1, Qt uses
        # integer variables, so you need a factor; the higher the factor, the
        # more precise are the results (2000 should suffice).

        # Set the media position to where the slider was dragged
        self.timer.stop()
        pos = self.positionslider.value()
        self.mediaplayer.set_position(pos / 2000.0)
        self.timer.start()

    def on_video_play_changed(self, pos):
        self.timer.stop()
        self.mediaplayer.set_position(pos / dict(self.parent.info.properties)['Frame count'])
        self.timer.start()

        self.mediaplayer.play()
        self.playbutton.setIcon(self.icons['PAUSE'])
        self.timer.start()
        self.is_paused = False
    def update_ui(self):
        '''Updates the user interface'''

        # Set the slider's position to its corresponding media position
        # Note that the setValue function only takes values of type int,
        # so we must first convert the corresponding media position.
        media_pos = int(self.mediaplayer.get_position() * 2000)
        self.positionslider.setValue(media_pos)
        total_time = self.mediaplayer.get_length() / 1000  # 总时间（以秒为单位）
        current_time = self.mediaplayer.get_time() / 1000  # 已经播放的时间（以秒为单位）

        total_time_str = time.strftime('%H:%M:%S', time.gmtime(total_time))
        current_time_str = time.strftime('%H:%M:%S', time.gmtime(current_time))

        self.total_time_label.setText(total_time_str)
        self.current_time_label.setText(current_time_str)
        # No need to call this function if nothing is played
        if not self.mediaplayer.is_playing():
            self.timer.stop()

            # After the video finished, the play button stills shows 'Pause',
            # which is not the desired behavior of a media player.
            # This fixes that 'bug'.
            if not self.is_paused:
                self.stop()


def main():
    '''Entry point for our simple vlc player
    '''
    app = QtWidgets.QApplication(sys.argv)
    player = VLCPlayer()
    player.show()
    player.resize(640, 480)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
