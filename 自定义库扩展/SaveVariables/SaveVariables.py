#-*- coding: utf8 -*-

from os.path import join
from datetime import date, datetime
import yaml, json
import os, time


class SaveVariables:

    def __init__(self):
        self.FilePath = None
        self.Stream_Read = None
        self.Stream = None
        self.Stream_Del = None

    def Set_VarPath(self, filepath):
        """
        设置变量文件保存的路径目录。
        必须先设置才能使用后面的关键字。

        参数:
         - FilePath： 文件路径目录

        例如:
           | Set VarPath | F:\\\Test_Data |
        """
        self.FilePath = filepath

        print u"设置变量文件保存路径目录成功！ %s" % self.FilePath

    #写变量文件
    def Save_Var(self, var_name, var_content):
        """
        往yaml文件中存入变量。
        必须先设置才能使用后面的关键字。

        参数:
         - var_name： 保存的变量名
         - var_content： 变量名对应的值

        例如:
           | Save Var | var1 | text |
        """
        document = {}
        document[str(var_name)] = unicode(var_content)

        var_file_path = self.FilePath + '\Variable_File.yaml'

        with open(var_file_path, 'a') as f_s:
            self.Stream_Read = file(var_file_path)   #只读
            s = yaml.load(self.Stream_Read)
            if hasattr(s, 'has_key'):
                if s.has_key(var_name):
                    s.update(document)
                    self.Stream_Del = file(var_file_path, "w")  #重写
                    yaml.dump(s, self.Stream_Del, default_flow_style=False)
                    print u"\t\n存在已知变量，重新写入变量文件！\t\n"
                else:
                    yaml.dump(document, file(var_file_path, "a"), default_flow_style=False)
            else:
                yaml.dump(document, file(var_file_path, "a"), default_flow_style=False)

        print u"\t\n成功写入变量文件！\t\n"

    #读变量
    def Read_Var(self, var_name):
        """
        从yaml文件中取出变量。
        必须先设置才能使用后面的关键字。

        参数:
         - var_name： 取出的变量名

        例如:
           | Read Var | var1 |
        """
        var_file_path = self.FilePath + '\Variable_File.yaml'
        self.Stream_Read = file(var_file_path)   #只读
        s = yaml.load(self.Stream_Read)
        if s:
            for item_value in s:
                if str(var_name) == item_value:
                    return s[var_name]
        return

    #写json文件
    def Save_Json(self, root_dir_name, content, times=None):
        """
        将json对象格式化后存入文件(文件保存名为tree.json)。

        参数:
         - root_dir_name： 文件保存的根目录名
         - content： json对象
         - times: 时间戳，用来对比两个json文件的差异（默认自动生成）

        例如:
           | Save Json | F:\\ | ${dict} |
        """
        dir_path = unicode(root_dir_name)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        if not times:
            str_times = time.strftime("%Y%m%d%H%M%S")
        else:
            str_times = times

        if not os.path.exists(dir_path + '\\' + str_times):
            os.mkdir(dir_path + '\\' + str_times)

        if not times:
            json_file_path = dir_path + '\\' + str_times + '\\tree.json'
        else:
            if not os.path.exists(dir_path + '\\' + str_times + '\\Diff'):
                os.mkdir(dir_path + '\\' + str_times + '\\Diff')
            json_file_path = dir_path + '\\' + str_times + '\\Diff\\tree.json'

        with open(json_file_path, 'w') as json_file:
            json_file.write(json.dumps(content))

        print u"成功写入Json文件！"
        return str_times

    def Read_Json(self, root_dir_name, times):
        """
        从json文件夹内读取json文件内容(文件名为tree.json)。

        参数:
         - root_dir_name： 文件保存的根目录名
         - times： 代表json的时间戳目录

        例如:
           | Read Json | F:\\ | ${times} |
        """
        dir_path = unicode(root_dir_name)
        json_file_path = dir_path + '\\' + times + '\\tree.json'
        with open(json_file_path) as json_file:
            data = json.load(json_file)
            return data


if __name__ == "__main__":
    pass


