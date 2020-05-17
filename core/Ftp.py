from ftplib import FTP  # 加载ftp模块
from ftplib import error_perm
import socket, os ,datetime
from conf.setting import *
from log.Log import log_info


class Ftpclient:
    def __init__(self):
        self.host = HOSTIP
        self.username = USERNAME
        self.password = PASSWORD
        self.port = PORT
        self.weekday = datetime.datetime.now().weekday()
        self.filelist = []
        self.ftp = FTP()

    @property
    def ftpconnect(self):
        """
        连接FTP服务器
        :return:
        """
        # ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
        self.ftp.encoding = 'utf-8'  # 解决中文编码问题，默认是latin-1
        try:
            self.ftp.connect(self.host, self.port)  # 连接
            self.ftp.login(self.username, self.password)  # 登录，如果匿名登录则用空串代替即可
            # print(ftp.getwelcome())  # 打印欢迎信息
        except(socket.error, socket.gaierror):  # ftp 连接错误
            return {'status': 0, 'info': 'cannot connect %s:%s' % (self.host, self.port)}
        except error_perm:  # 用户登录认证错误
            return {'status': 0, 'info': "user Authentication failed"}
        return {'status': 1, 'info': 'Connection successful'}


    def is_same_size(self, localfile, remotefile):
        """
        对比本地文件和远程文件是否一致，根据返回值进行判断是否更新备份，1、不更新 0、更新
        :param localfile:
        :param remotefile:
        :return:
        """
        try:
            remotefile_size = self.ftp.size(remotefile)
        except:
            remotefile_size = -1
        try:
            localfile_size = os.path.getsize(localfile)
        except:
            localfile_size = -1
        if self.weekday in FULLWEEKDAY:
            return 0
        if remotefile_size == localfile_size:
            return 1
        else:
            return 0

    def upload_file(self, localfile, remotefile):
        """
        将本地文件上传至FTP服务器
        :param localfile: 本地文件
        :param remotefile: 远程文件
        :return:
        """
        if not os.path.isfile(localfile):
            return
        if self.is_same_size(localfile, remotefile):
            return
        file_handler = open(localfile, 'rb')
        res = self.ftp.storbinary('STOR %s' % remotefile, file_handler)
        if res.find('226') != -1:
            self.filelist.append(remotefile)
            print("Success upload file complete " + localfile)
            log_info("Success upload file complete " + localfile)
        file_handler.close()




