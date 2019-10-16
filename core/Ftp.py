from ftplib import FTP  # 加载ftp模块
from ftplib import error_perm
import socket
from conf.setting import *
from log.Log import log_info


class Ftpclient:
    def __init__(self):
        self.host = HOSTIP
        self.username = USERNAME
        self.password = PASSWORD
        self.port = PORT

    @property
    def ftpconnect(self):
        ftp = FTP()
        # ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
        ftp.encoding = 'utf-8'  # 解决中文编码问题，默认是latin-1
        try:
            ftp.connect(self.host, self.port)  # 连接
            ftp.login(self.username, self.password)  # 登录，如果匿名登录则用空串代替即可
            # print(ftp.getwelcome())  # 打印欢迎信息
        except(socket.error, socket.gaierror):  # ftp 连接错误
            return {'status': 0, 'info': 'cannot connect %s:%s' % (self.host, self.port)}
        except error_perm:  # 用户登录认证错误
            return {'status': 0, 'info': "user Authentication failed"}
        return {'status':1,'info':ftp}

    def downloadfile(self, remotepath, localpath):
        """
         下载文件
        :param ftp:
        :param remotepath:
        :param localpath:
        :return:
        """
        bufsize = 1024  # 设置缓冲块大小
        fp = open(localpath, 'wb')  # 以写模式在本地打开文件

        res = self.ftpconnect.get('info').retrbinary(
            'RETR ' + remotepath,
            fp.write,
            bufsize)  # 接收服务器上文件并写入本地文件
        if res.find('226') != -1:
            log_info("download file complete" + localpath)
            print(" Success download file complete" + localpath)
        self.ftpconnect.get('info').set_debuglevel(0)  # 关闭调试
        fp.close()  # 关闭文件

    def uploadfile(self, remotepath, localpath):
        """
        上传文件
        :param ftp:
        :param remotepath:
        :param localpath:
        :return:
        """
        bufsize = 1024
        fp = open(localpath, 'rb')
        res = self.ftpconnect.get('info').storbinary('STOR ' + remotepath, fp, bufsize)  # 上传文件
        if res.find('226') != -1:
            log_info("upload file complete " + remotepath)
            print("Success upload file complete " + remotepath)
        self.ftpconnect.get('info').set_debuglevel(0)
        fp.close()

