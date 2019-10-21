from conf.setting import *
from core.filelist import Backup
from core.public import send_message,pub
from concurrent.futures import ThreadPoolExecutor
from core.Ftp import Ftpclient
import os, datetime, json


def foo(func):
    def times():
        start_time = datetime.datetime.now()
        func()
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        pub("Time for this backup %s" % duration)

    return times



def ftp_theadpool(func, file_list, remotedirname):
    """
    通过线程池调用上传文件列表
    :param func:
    :param file_list:
    :return:
    """
    pool = ThreadPoolExecutor(FtpTheadpoolNum)
    for localpath in file_list:
        filename = os.path.basename(localpath)
        pool.submit(func, os.path.join(remotedirname, filename), localpath)
    pool.shutdown()

@foo
def start():
    """
    主进程函数
    :return:
    """
    ftpclient = Ftpclient()
    message_list = []
    try:
        if ftpclient.ftpconnect.get('status'):
            backup = Backup()
            newfilelist = backup.newfilelist
            if newfilelist == []:
                pub('No file requires backup!!!')
                message_list = [{'name': 'info', 'info': 'No file requires backup!!!'}]
            else:
                filelist = ftpclient.ftpconnect.get('info').nlst(REMOTEPATH)
                dirname = str(datetime.date.today())
                remotedirname = os.path.join(REMOTEPATH, dirname)
                if dirname not in filelist:  # 创建目录
                    res = ftpclient.ftpconnect.get('info').mkd(remotedirname)
                    pub('Successfully created file %s' % res)
                ftp_theadpool(ftpclient.uploadfile, newfilelist, remotedirname)
                pwd_path = ftpclient.ftpconnect.get('info').nlst(remotedirname)
                for localpath in newfilelist:
                    message = {}
                    localfile = os.path.basename(localpath)
                    if localfile in pwd_path:
                        message["name"] = localpath
                        message['info'] = " Upload success"
                        message_list.append(message)
                    else:
                        message['name'] = localpath
                        message['info'] = " Upload failed"
                        message_list.append(message)
                # message_list.append({'name': '远程备份目录列表', 'info': '、'.join(pwd_path)})
            ftpclient.ftpconnect.get('info').quit()
        else:
            message_list = [{'name': 'ERROR', 'info': ftpclient.ftpconnect.get('info')}]
            pub(ftpclient.ftpconnect.get('info'), 'error')
        send_message(message_list)
        # print(message_list)
    except Exception as e:
        pub(e, 'error')
