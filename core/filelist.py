import os, datetime, json
from conf.setting import *
from concurrent.futures import ThreadPoolExecutor


class Backup:
    newfilelist = []

    def __init__(self):
        self.fullback()

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
            pool.submit(func, file, historyfiledic)
        pool.shutdown()

    def filter(self, file, historyfiledic):
        """
        对备份文件进行过滤避免重复上传，只上传新增的文件
        :return:newfilelist
        """
        if file in historyfiledic['historylist']:
            pass
        else:
            self.newfilelist.append(file)
            historyfiledic['historylist'].append(file)

    def fullback(self):
        """
        判断是否进行全备
        :param:historyfilepath
        :return:
        """
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
