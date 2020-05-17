from conf.setting import *
from core.public import send_message, pub
from core.Ftp import Ftpclient
import os, datetime


def upload_files(ftpclient, localdir, remotedir):
    """
    上传文件到ftp服务器
    :param ftpclient:
    :param localdir:
    :param remotedir:
    :return:
    """
    if not os.path.isdir(localdir):
        return
    localnames = os.listdir(localdir)
    try:
        ftpclient.ftp.cwd(remotedir)
    except:
        ftpclient.ftp.mkd(remotedir)
        ftpclient.ftp.cwd(remotedir)
    for item in localnames:
        src = os.path.join(localdir, item)
        if src in EXCLUDE:
            # 增加排除目录或文件
            continue
        if os.path.isdir(src):
            try:
                ftpclient.ftp.mkd(item)
            except:
                pass
            upload_files(ftpclient, src, item)
        else:
            ftpclient.upload_file(src, item)
    ftpclient.ftp.cwd('..')


def filelistpath(ftpclient):
    """
    递归获取本地所有目录路径
    :param ftpclient:
    :return:
    """
    try:
        for pathlist in BACKUPDIR:
            localdir = pathlist['localpath']
            remotedir = pathlist['remotepath']
            if not remotedir:
                remotedir = os.path.split(localdir)[-1]
            upload_files(ftpclient, localdir, remotedir)
        return 1
    except:
        pub('Check that the configuration file is correct','error')
        send_message('Check that the configuration file is correct')
        return 0

def start():
    """
    主进程函数
    :return:
    """
    try:
        ftpclient = Ftpclient()
        if ftpclient.ftpconnect.get('status'):
            start_time = datetime.datetime.now()
            ret = filelistpath(ftpclient)
            end_time = datetime.datetime.now()
            duration = end_time - start_time
            pub("Time for this backup %ss" % duration.seconds)
            if ret:
                send_message(
                    '本次备份文件列表详情:\n备份成功，本次共备份%s个文件,耗时%ss。' % (
                        len(ftpclient.filelist), duration.seconds))
                print(
                    '本次备份文件列表详情:\n备份成功，本次共备份%s个文件,耗时%ss。' % (
                        len(ftpclient.filelist), duration.seconds))
        else:
            pub(ftpclient.ftpconnect.get('info'), 'error')
            send_message('ERROR' + ftpclient.ftpconnect.get('info'))
    except Exception as e:
        pub(e, 'error')
        send_message('ERROR' + e)
