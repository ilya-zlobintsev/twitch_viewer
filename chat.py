from dataclasses import dataclass
import socket


class Chat:
    def __init__(self, oauth_token, username):
        self.token = f"oauth:{oauth_token}"
        self.username = username

    def connect(self, channel):
        self.irc = socket.socket()
        self.irc.connect(("irc.chat.twitch.tv", 6667))

        self.irc.send(f"PASS {self.token}\n".encode("utf-8"))
        self.irc.send(f"NICK {self.username}\n".encode("utf-8"))
        self.irc.send(f"JOIN #{channel}\n".encode("utf-8"))

    def listen(self):
        response = self.irc.recv(2048).decode("utf-8")
        if response.startswith('PING'):
            self.irc.send("PONG\n".encode("utf-8"))
            return

        username = response[1:response.index('!')]
        message = response[response.index(':', 1) + 1:]
        return ChatMessage(username, message)


@dataclass
class ChatMessage:
    username: str
    message: str
