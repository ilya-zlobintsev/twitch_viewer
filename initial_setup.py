from PyQt5.QtWidgets import QDialog, QSizePolicy
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtCore import QUrl

from twitch_api import TwitchApi


CLIENT_ID = "fkdschoxmb5ls6pb767kn1cgx4mvyu"

class InitialSetupDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InitialSetupDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(500)
        self.setFixedHeight(400)
        self.setWindowTitle("Authenticate")

        self.webview = QWebView(self)
        self.webview.setFixedWidth(500)
        self.webview.setFixedHeight(400)

        self.webview.urlChanged.connect(self.redirected)

        request_url = "https://id.twitch.tv/oauth2/authorize?response_type=token+id_token&client_id={}&scope=openid%20chat:read%20chat:edit&redirect_uri=http://localhost".format(CLIENT_ID)

        self.webview.setUrl(QUrl(request_url))

        self.token = None

    def redirected(self, qurl):
        if (qurl.url()[:32] == "https://localhost/#access_token=") or (qurl.url()[:31] == "http://localhost/#access_token="):
            self.token = qurl.url()[32:qurl.url().index('&')]
            self.accept()

            api = TwitchApi(CLIENT_ID, self.token)
            self.username = api.get_users_by_login()["data"][0]["display_name"]

    def exec_(self):
        super(InitialSetupDialog, self).exec_()
        if self.token is not None:
            return {"client_id": CLIENT_ID,
                    "oauth_token": self.token,
                    "username": self.username}
