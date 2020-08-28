from PyQt5.QtWidgets import QTreeView, QHeaderView
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QBrush, QColor

from workers import FollowingLoader


class FollowingTreeView(QTreeView):
    def __init__(self, twitch_api):
        super(FollowingTreeView, self).__init__()
        self.twitch_api = twitch_api

        self.setFixedWidth(200)

        self.model = QStandardItemModel(0, 2, self)
        self.setModel(self.model)

        self.setRootIsDecorated(False)
        self.setHeaderHidden(True)

        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.following_loader = FollowingLoader(self.twitch_api)
        self.following_loader.output.connect(self.add_item)
        self.following_loader.start()

    def add_item(self, stream):
        name_item = QStandardItem(stream["user_name"])
        viewcount_item = QStandardItem(str(stream["viewer_count"]))
        viewcount_item.setForeground(QBrush(QColor("#dd255c")))
        self.model.appendRow([name_item, viewcount_item])
