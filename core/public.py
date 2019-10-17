from conf.setting import *
from log.Log import log_info

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
        ret = mymail.send_to(message_list)
        log_info(ret)
    if WECHAT:
        from  core.wechat import Wechat
        mywechat = Wechat()
        ret = mywechat.send_message(message_list)
        log_info(ret)
    if DINGTALK:
        from core.dingding import DingTalk
        dingtalk = DingTalk
        ret = dingtalk.send(message_list)
        log_info(ret)