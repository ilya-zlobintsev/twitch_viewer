import requests
import json


class TwitchApi:
    def __init__(self, client_id, oauth):
        self.client_id = client_id
        self.oauth = oauth
        self.headers = {"Client-ID": self.client_id,
                        "Authorization": "Bearer " + self.oauth}
        print("Initialized with headers " + json.dumps(self.headers))

    def get_streams(self, user_ids=None, first=100):
        url = "https://api.twitch.tv/helix/streams"

        payload = [("first", first)]
        if user_ids is not None:
            for user_id in user_ids:
                payload.append(("user_id", user_id))

        response = requests.get(url, headers=self.headers, params=payload)

        #print("requested to " + response.url)

        return response.json()

    def get_all_streams(self, user_ids):
        streams = []

        for i in range(0, len(user_ids), 100):
            result = self.get_streams(user_ids[i:i+100])

            streams.extend(result["data"])

        return sorted(streams, key=lambda k: k["viewer_count"], reverse=True)

    def get_users_by_id(self, user_ids):
        url = "https://api.twitch.tv/helix/users"

        payload = []
        for user_id in user_ids:
            payload.append(("id", user_id))

        response = requests.get(url, headers=self.headers, params=payload)

        #print("request to " + response.url + " " + str(response.status_code))

        return response.json()

    def get_users_by_login(self, user_logins=None, amount=100, cursor=None):
        url = "https://api.twitch.tv/helix/users"

        payload = { "first": amount }
        if cursor is not None:
            payload.append(("cursor", cursor))

        if user_logins is not None:
            for login in user_logins:
                payload.append(("login", login))

        response = requests.get(url, headers=self.headers, params=payload)

        #print("request to " + response.url + " " + str(response.status_code))

        return response.json()

    def get_follows_from(self, user_id, amount=100, cursor=None):
        url = "https://api.twitch.tv/helix/users/follows"

        payload = { "from_id": user_id, "first": amount}

        if cursor is not None:
            payload["after"] = cursor

        response = requests.get(url, headers=self.headers, params=payload)

        #print("request to " + response.url + " " + str(response.status_code))

        return response.json()

    def get_all_follows_from(self, user_id):
        result = self.get_follows_from(user_id, 100)
        i = 100
        cursor = result["pagination"]["cursor"]

        results = result["data"]

        while i < result["total"]:
            result = self.get_follows_from(user_id, 100, cursor)
            results.extend(result["data"])
            cursor = result["pagination"]["cursor"]

            i += 100

        return results

    def get_followed_streams(self):
        user_id = self.get_users_by_login()["data"][0]["id"]
        follows = self.get_all_follows_from(user_id)

        following_ids = []
        for follow in follows:
            following_ids.append(follow["to_id"])
        
        streams = self.get_all_streams(following_ids)
        return streams

    def get_emotes_in_channel(self, channel_id):
        url = "https://api.twitchemotes.com/api/v4/channels/" + channel_id

        response = requests.get(url)
        return response.json()

    def get_ffz_emotes_in_channel(self, channel_name):

        url = "https://api.frankerfacez.com/v1/room/" + channel_name.lower()
        response = requests.get(url).json()

        emote_set = response["room"]["set"]
        emotes = {}
        for emote in response["sets"][str(emote_set)]["emoticons"]:
            emotes[emote["name"]] = emote["urls"]["1"]

        return emotes
