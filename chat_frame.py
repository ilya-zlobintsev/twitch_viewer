from PyQt5.QtWidgets import QVBoxLayout, QLabel, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt

from workers import ChatWorker


class ChatFrame(QScrollArea):
    def __init__(self):
        super(ChatFrame, self).__init__()

        self.setMaximumWidth(300)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        self.messagesLayout = QVBoxLayout()

        self.setLayout(self.messagesLayout)

    def connect(self, oauth_token, username, channel):
        self.chat_worker = ChatWorker(oauth_token, username, channel)
        self.chat_worker.output.connect(self.add_message)
        self.chat_worker.start()

    def add_message(self, msg):
        label = QLabel()
        label.setMinimumHeight(50)
        label.setText(f"{msg.username}: {msg.message}")
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.messagesLayout.addWidget(label)
