from conf.setting import *
import os
import requests
import json


class Wechat:
    def __init__(self):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.touser = '|'.join(touser)
        self.agentid = agentid
        self.filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf', 'wechat.json')

    @property
    def get_access_token(self):
        get_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (
            self.corpid, self.corpsecret)
        ret = requests.get(get_url, verify=False).json()
        if ret.get('errcode') != 0:
            return False
        else:
            Token = ret['access_token']
            file = open(self.filepath, 'w')
            json.dump(ret, file)
            file.close()
            return Token

    def send_message(self, message):
        try:
            file = open(self.filepath, 'r')
            Token = json.load(file).get('access_token')
            file.close()
        except:
            Token = self.get_access_token
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % Token
        Data = {
            "touser": self.touser,  # 企业号中的用户帐号，在zabbix用户Media中配置，如果配置不正常，将按部门发送。
            # "totag": Tagid,                                # 企业号中的标签id，群发使用（推荐）
            # "toparty": Partyid,                             # 企业号中的部门id，群发时使用。
            "msgtype": "text",  # 消息类型。
            "agentid": self.agentid,  # 企业号中的应用id。
            "text": {
                "content": 'FTP备份上传回执信息：' + '\n' + message
            },
            "safe": "0"
        }
        n = 0
        r = requests.post(url=send_url, data=json.dumps(Data), verify=False)
        while r.json().get('errcode') != 0 and n < 4:
            n += 1
            Token = self.get_access_token
            if Token:
                Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
                r = requests.post(url=Url, data=json.dumps(Data), verify=False)
        return r.json()
