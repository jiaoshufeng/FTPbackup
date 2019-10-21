import os, datetime, json
from conf.setting import *
from concurrent.futures import ThreadPoolExecutor
import hashlib
from core.public import pub

class Backup:
    newfilelist = []

    def __init__(self):
        self.fullback()

    def getmd5(self, file):
        m = hashlib.md5()
        with open(file, 'rb') as f:
            for line in f:
                m.update(line)
        md5code = m.hexdigest()
        return {'path': file, 'md5': md5code}

    def file_list(self, backdir, filelist=[]):
        """
        获取备份目录下所有的文件列表
        :param backdir:
        :param filelist:
        :return: filelist
        """
        for i in os.listdir(backdir):
            temp_dir = os.path.join(backdir, i)
            if os.path.isdir(temp_dir):
                self.file_list(temp_dir, filelist)
            else:
                filelist.append(temp_dir)
        return filelist

    def filter_theadpool(self, func, file_list, historyfiledic):
        """
        通过线程池对历史上传数据进行过滤
        :param func:
        :param file_list:
        :param historyfiledic:
        :return:
        """
        pool = ThreadPoolExecutor(FilterTheadpoolNum)
        for file in file_list:
            files = self.getmd5(file)
            pool.submit(func, files, historyfiledic)
        pool.shutdown()

    def filter(self, files, historyfiledic):
        """
        对备份文件进行过滤避免重复上传，只上传新增的文件
        :return:newfilelist
        """
        if files in historyfiledic['historylist']:
            pass
        else:
            self.newfilelist.append(files['path'])
            historyfiledic['historylist'].append(files)

    def fullback(self):
        """
        判断是否进行全备
        :param:historyfilepath
        :return:
        """
        try:
            d = datetime.datetime.now()
            weekday = d.weekday()
            historyfilepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf', 'historyfile.json')
            if weekday in FULLWEEKDAY:
                with open(historyfilepath, 'w') as historyfilename:
                    json.dump({"historylist": []}, historyfilename)
            with open(historyfilepath, 'r') as historyfilename:
                historyfiledic = json.load(historyfilename)
            self.filter_theadpool(self.filter, self.file_list(BACKUPDIR), historyfiledic)
            with open(historyfilepath, 'w') as historyfilename2:
                json.dump(historyfiledic, historyfilename2)
        except Exception as e:
            pub(e,'error')
