from conf.setting import *
from log.Log import log_info

def send_message(message):
    """
    发送信息回执至第三方系统（微信，邮箱，钉钉）
    :param message_list:
    :return:
    """
    if EMAIL:
        from core.Email import Mymail
        mymail = Mymail()
        ret = mymail.send_to(message)
        pub(ret)
    if WECHAT:
        from  core.wechat import Wechat
        mywechat = Wechat()
        ret = mywechat.send_message(message)
        pub(ret)
    if DINGTALK:
        from core.dingding import DingTalk
        dingtalk = DingTalk
        ret = dingtalk.send(message)
        pub(ret)

def pub(message, level='info'):
    """

    :param message:
    :param level:
    :return:
    """
    print(message)
    log_info(message, level)