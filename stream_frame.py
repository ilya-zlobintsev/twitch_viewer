from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStyle
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl

from workers import StreamLinkLoader


class StreamFrame(QWidget):
    def __init__(self):
        super(StreamFrame, self).__init__()
        rootLayout = QVBoxLayout()

        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)

        controlLayout = QHBoxLayout()

        playpause_button = QPushButton()
        playpause_button.setFixedWidth(50)
        playpause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        playpause_button.clicked.connect(self.toggle_play)

        controlLayout.addWidget(playpause_button)
        rootLayout.addWidget(self.video_widget)
        rootLayout.addLayout(controlLayout)

        self.setLayout(rootLayout)

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

    def open_raw_link(self, link):
        self.media_player.setMedia(QMediaContent(QUrl(link)))
        self.media_player.play()

