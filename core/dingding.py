import requests
from conf.setting import *


class DingTalk:
    """
    封装一个钉钉自定义机器人的类
    """
    def __init__(self):
        self.url = webhook
        self.headers = {
            'Content-Type': 'application/json',
            'charset': 'utf-8'
        }

    def send(self, content):
        """
        发送信息
        :param content: 消息文本内容
        :return: 回执
        """
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

