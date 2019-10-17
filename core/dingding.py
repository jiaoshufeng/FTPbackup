import requests
from conf.setting import *


class DingTalk:

    def __init__(self):
        self.url = webhook
        self.headers = {
            'Content-Type': 'application/json',
            'charset': 'utf-8'
        }

    def send(self, content):
        msg = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": [
                ],
                "isAtAll": "false"
            }
        }
        ret = requests.post(url=self.url, headers=self.headers, json=msg).text
        return ret

