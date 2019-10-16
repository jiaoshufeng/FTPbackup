import os

class Backup:

    def file_list(self,backdir,filelist=[]):
        """
        获取备份目录下所有的文件列表
        :param backdir:
        :param filelist:
        :return: filelist
        """
        # list=[]
        # ret = os.listdir(self.backdir)
        # for file in ret:
        #     ret = os.path.join(self.backdir, file)
        #     if os.path.isfile(ret):
        #         list.append(ret,filelist)
        # return list
        for i in os.listdir(backdir):
            temp_dir = os.path.join(backdir, i)
            if os.path.isdir(temp_dir):
                self.file_list(temp_dir, filelist)
            else:
                filelist.append(temp_dir)
        return filelist



