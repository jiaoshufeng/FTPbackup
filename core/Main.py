from conf.setting import *
from core.public import send_message, pub
from concurrent.futures import ThreadPoolExecutor
from core.Ftp import Ftpclient
import os, datetime


def foo(func):
    """
    计算备份时间
    :param func:
    :return:
    """

    def times(*args, **kwargs):
        start_time = datetime.datetime.now()
        func(*args, **kwargs)
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        pub("Time for this backup %s" % duration.seconds)
        return duration.seconds

    return times


def ftp_theadpool(func, src, item):
    """
    通过线程池调用上传文件列表
    :param func:
    :param file_list:
    :return:
    """
    pool = ThreadPoolExecutor(FtpTheadpoolNum)
    pool.submit(func, src, item)
    pool.shutdown()


@foo
def upload_files(ftpclient, localdir, remotedir):
    """
    递归目录
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
        if os.path.isdir(src):
            try:
                ftpclient.ftp.mkd(item)
            except:
                pass
            upload_files(ftpclient, src, item)
        else:
            ftp_theadpool(ftpclient.upload_file, src, item)
    ftpclient.ftp.cwd('..')


def start():
    """
    主进程函数
    :return:
    """
    try:
        ftpclient = Ftpclient()
        if ftpclient.ftpconnect.get('status'):
            ret = upload_files(ftpclient, localdir=BACKUPDIR, remotedir=REMOTEPATH)
            if ftpclient.filelist == []:
                send_message('本次备份文件列表详情:\n' + '没有需要备份的文件')
                print('本次备份文件列表详情:\n' + '没有需要备份的文件')
            else:
                send_message(
                    '本次备份文件列表详情:\n备份成功，本次共备份%s个文件,耗时%ss。\n%s' % (
                        len(ftpclient.filelist), ret, ','.join(ftpclient.filelist)))
                print(
                    '本次备份文件列表详情:\n备份成功，本次共备份%s个文件,耗时%ss。\n%s' % (
                        len(ftpclient.filelist), ret, ','.join(ftpclient.filelist)))
        else:
            pub(ftpclient.ftpconnect.get('info'), 'error')
            send_message('ERROR' + ftpclient.ftpconnect.get('info'))
    except Exception as e:
        pub(e, 'error')
        send_message('ERROR' + e)
