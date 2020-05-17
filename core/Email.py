import smtplib
from email.mime.text import MIMEText
from conf.setting import *


class Mymail:
    """
    封装一个邮件的类
    """
    def __init__(self):
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        self.sender = sender
        self.receivers = receivers

    def message(self, message_list):
        """
        对消息列表进行格式化处理
        :param message_list:接受到的消息列表
        :return: message
        """
        mail_msg = """
            <div><span>标题:FTP备份通知</span></div>
            <div><span>%s</span></div>
            """ % (message_list)
        message = MIMEText(mail_msg, 'html', 'utf-8')
        # 邮件主题
        message['Subject'] = 'FTP备份通知消息'
        # 发送方信息
        message['From'] = self.sender
        # 接受方信息
        message['To'] = self.receivers[0]
        return message

    def send_to(self, message_list):
        """
        发送消息
        :param message_list:
        :return: 回执
        """
        try:
            # 连接到服务器
            smtpObj = smtplib.SMTP_SSL(mail_host)
            # 登录到服务器
            smtpObj.login(mail_user, mail_pass)
            # 发送
            smtpObj.sendmail(
                self.sender, self.receivers, self.message(message_list).as_string())
            # 退出
            smtpObj.quit()
            return 'Mail sent successfully'
        except smtplib.SMTPException as e:
            return 'Mail failed to send'
