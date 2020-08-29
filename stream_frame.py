from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QPushButton,
                             QStyle, QGridLayout, QGraphicsOpacityEffect)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QPropertyAnimation

from workers import StreamLinkLoader


class StreamFrame(QWidget):
    def __init__(self):
        super(StreamFrame, self).__init__()
        rootLayout = QGridLayout()

        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)

        self.controlWidget = QWidget()
        controlLayout = QHBoxLayout()
        self.controlWidget.setLayout(controlLayout)

        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.7)
        self.controlWidget.setGraphicsEffect(self.opacity_effect)

        self.playpause_button = QPushButton()
        self.playpause_button.setFixedWidth(50)
        self.playpause_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.playpause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playpause_button.clicked.connect(self.toggle_play)
        self.playpause_button.hide()

        controlLayout.addWidget(self.playpause_button)
        rootLayout.addWidget(self.video_widget, 0, 0)
        rootLayout.addWidget(self.controlWidget, 0, 0, Qt.AlignBottom)

        self.setLayout(rootLayout)

    def enterEvent(self, e):
        self.anim = QPropertyAnimation(self.controlWidget, b"maximumHeight")
        self.anim.setDuration(100)
        self.anim.setStartValue(0)
        self.anim.setEndValue(50)
        self.anim.start()

    def leaveEvent(self, e):
        self.anim = QPropertyAnimation(self.controlWidget, b"maximumHeight")
        self.anim.setDuration(100)
        self.anim.setStartValue(50)
        self.anim.setEndValue(0)
        self.anim.start()

    def toggle_play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            link = self.media_player.media().canonicalUrl()
            self.media_player.setMedia(QMediaContent())
            self.open_raw_link(link)

    def open_stream(self, stream):
        self.link_loader = StreamLinkLoader("http://twitch.tv/" + stream)
        self.link_loader.output.connect(self.open_raw_link)
        self.link_loader.start()

        self.playpause_button.show()

    def open_raw_link(self, link):
        self.media_player.setMedia(QMediaContent(QUrl(link)))
        self.media_player.play()

