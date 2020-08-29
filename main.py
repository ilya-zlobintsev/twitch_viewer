#!/usr/bin/python
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout

import sys
import os
import json
from pathlib import Path

from following_treeview import FollowingTreeView
from stream_frame import StreamFrame
from chat_frame import ChatFrame

from twitch_api import TwitchApi


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.load_config()
        self.twitch_api = TwitchApi(self.config["client_id"],
                                    self.config["oauth_token"])
        self.build_ui()

    def build_ui(self):
        self.resize(800, 500)

        root_widget = QWidget(self)
        self.setCentralWidget(root_widget)

        main_layout = QHBoxLayout()

        self.following_tree_view = FollowingTreeView(self.twitch_api)
        self.following_tree_view.selectionModel().selectionChanged.connect(self.activate_stream)

        self.stream_frame = StreamFrame()
        self.chat_frame = ChatFrame()

        main_layout.addWidget(self.following_tree_view, stretch=1)
        main_layout.addWidget(self.stream_frame, stretch=4)
        main_layout.addWidget(self.chat_frame, stretch=2)

        root_widget.setLayout(main_layout)

    def activate_stream(self):
        selected = self.following_tree_view.selectedIndexes()[0].data().replace(' ', '')
        self.stream_frame.open_stream(selected)

        self.chat_frame.connect(self.config["oauth_token"], self.config["username"], selected)

    CONFIG_PATH = str(Path.home()) + "/.config/twitch_viewer/settings.json"

    def load_config(self):
        try:
            self.config = json.load(open(self.CONFIG_PATH, "r"))
        except FileNotFoundError:
            from initial_setup import InitialSetupDialog
            dialog = InitialSetupDialog(self)
            config = dialog.exec_()

            if config is not None:
                self.config = config
                self.write_config()
            else:
                sys.exit()

    def write_config(self):
        config_folder = os.path.dirname(self.CONFIG_PATH)
        if not os.path.exists(config_folder):
            os.makedirs(config_folder)
        json.dump(self.config, open(self.CONFIG_PATH, "w"))


app = QApplication(sys.argv)
win = MainWindow()
win.show()
app.exec_()
