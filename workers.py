from PyQt5.QtCore import QThread, pyqtSignal

from youtube_dl import YoutubeDL


class FollowingLoader(QThread):
    output = pyqtSignal(dict)

    def __init__(self, twitch_api):
        QThread.__init__(self)

        self.twitch_api = twitch_api

    def run(self):
        follows = self.twitch_api.get_followed_streams()

        for follow in follows:
            self.output.emit(follow)


class StreamLinkLoader(QThread):
    output = pyqtSignal(str)

    def __init__(self, stream_url):
        QThread.__init__(self)

        self.stream_url = stream_url

    def run(self):
        ydl = YoutubeDL()
        info = ydl.extract_info(self.stream_url, download=False)
        video_stream_link = info.get("url", None)
        self.output.emit(video_stream_link)
