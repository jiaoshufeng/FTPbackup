from conf.setting import *
from core.filelist import Backup
from core.public import send_message
from concurrent.futures import ThreadPoolExecutor
from core.Ftp import Ftpclient
from log.Log import log_info
import os, datetime, json

newfilelist = []


def pub(message, level='info'):
    print(message)
    log_info(message, level)



def filter_theadpool(func, file_list, historyfiledic):
    """
    通过线程池对历史上传数据进行过滤
    :param func:
    :param file_list:
    :param historyfiledic:
    :return:
    """
    pool = ThreadPoolExecutor(FilterTheadpoolNum)
    for file in file_list:
        pool.submit(func, file, historyfiledic)
    pool.shutdown()


def filter(file, historyfiledic):
    """
    对备份文件进行过滤避免重复上传，只上传新增的文件
    :return:newfilelist
    """
    if file in historyfiledic['historylist']:
        pass
    else:
        newfilelist.append(file)
        historyfiledic['historylist'].append(file)


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


def fullback():
    """
    判断是否进行全备
    :param:historyfilepath
    :return:
    """
    d = datetime.datetime.now()
    weekday = d.weekday()
    historyfilepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf', 'historyfile.json')
    if weekday == FULLWEEKDAY:
        with open(historyfilepath, 'w') as historyfilename:
            json.dump({"historylist": []}, historyfilename)
    dirpath = Backup()
    file_list = dirpath.file_list(BACKUPDIR)
    with open(historyfilepath, 'r') as historyfilename:
        historyfiledic = json.load(historyfilename)
    filter_theadpool(filter, file_list, historyfiledic)
    with open(historyfilepath, 'w') as historyfilename2:
        json.dump(historyfiledic, historyfilename2)


def start():
    """
    主进程函数
    :return:
    """
    fullback()
    ftpclient = Ftpclient()
    message_list = []
    try:
        if newfilelist == []:
            pub('No file requires backup!!!')
            message_list = [{'name': 'info', 'info': 'No file requires backup!!!'}]
        else:
            if ftpclient.ftpconnect.get('status'):
                filelist = ftpclient.ftpconnect.get('info').nlst(REMOTEPATH)
                dirname = str(datetime.date.today())
                remotedirname = os.path.join(REMOTEPATH, dirname)
                if dirname not in filelist:  # 创建目录
                    res = ftpclient.ftpconnect.get('info').mkd(remotedirname)
                    log_info('Successfully created file %s' % res)
                    print('Successfully created file', res)
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
        pub(e,'error')
