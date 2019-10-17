from conf.setting import *


def send_message(message_list):
    """
    发送信息回执至第三方系统（微信，邮箱，钉钉）
    :param message_list:
    :return:
    """
    info_list = []
    for message in message_list:
        info = message.get('name')+':'+message.get('info')
        info_list.append(info)
    message_list = '\n'.join(info_list)
    if EMAIL:
        from core.Email import Mymail
        mymail = Mymail()
        mymail.send_to(message_list)
    if WECHAT:
        from  core.wechat import Wechat
        mywechat = Wechat()
        mywechat.send_message(message_list)
    if DINGTALK:
        from core.dingding import DingTalk
        dingtalk = DingTalk
        dingtalk.send(message_list)