#!/usr/bin/python
#coding=utf-8

import os, shutil
import _winreg


class UpdateLib:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.abspath("__file__"))
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Python\PythonCore\2.7\InstallPath")
        name, value, type = _winreg.EnumValue(key, 0)
        self.python_install_path = value
        self.python_path = "{}Lib\\site-packages\\".format(self.python_install_path)

    def get_dir_file(self):
        """遍历路径
        返回：遍历后的路径目录和对应的目录下的文件名列表。
        """
        path_dict = {}
        for i in os.listdir(self.dir_path):
            path = self.dir_path + "/{}".format(i)
            if os.path.isdir(path) and i != ".idea" and i != ".svn":
                file_name = os.listdir(os.path.abspath(path))
                file_name = [a for a in file_name if a != ".svn"]
                path_dict.setdefault(os.path.abspath(path), file_name)
        return path_dict

    def check_lib_path(self, lib_name):
        """检查robot框架的官方库安装路径是否正确
        返回： 如果False 则会带上路径名
        """
        easy_install_file = self.python_path + "{}".format("easy-install.pth")
        if os.path.exists(easy_install_file):
            with open(easy_install_file) as install_file:
                file_content = install_file.readlines()
            for i in file_content:
                if str(lib_name).lower() in i:
                    i = i.replace("\n", "").split("/")[-1]
                    return False, i

        return True, ""

    def get_update_path(self, file_path):
        """返回 update.txt 中的文件列表内容"""
        content_list = []
        with open(file_path + "/update.txt") as str_file:
            file_content = str_file.readlines()
        for content in file_content:
            if content != "\n":
                content_list.append(content.replace("\n", ""))
        return content_list

    def copy_file_or_dir(self, src, dst):
        """
        :param src:
        :param dst:
        :return:
        """
        copy_name = dst.split("\\")[-1]
        # 如果内容是个目录，则 拷贝目录下的所有文件。 update.txt 规定了如果只是单个文件的话就写成目录路径的形式，如果多个文件就写成文件路径的形式。
        if os.path.isdir(os.path.abspath(dst)):
            for j in src[1]:
                shutil.copy(src[0] + "/{}".format(j), dst)
        # 如果是文件，就拷贝单个文件
        else:
            shutil.copyfile(src[0] + "/{}".format(copy_name), dst)

        print u"更新： {}".format(os.path.abspath(dst))

    def update_files(self):
        """更新文件或目录"""
        for path in self.get_dir_file().items():
            # 如果目录中没有 update.txt 则表示要拷贝整个目录
            if "update.txt" not in path[1]:
                dir_path = self.python_path + "{}".format(path[0].decode("gbk").split("\\")[-1])
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)

                shutil.copytree(path[0], dir_path)
                print u"更新： {}".format(dir_path)

            else:
                update_file_list = self.get_update_path(path[0])
                for i in update_file_list:
                    i = str(i).replace('C:\\Python27\\', self.python_install_path)   # 替换真实的目录路径，有可能python不是安装在C盘
                    lib_path_ok = self.check_lib_path(i.split("\\")[4])   # 检查标准库的安装路径是否正确
                    if lib_path_ok[0] or i.split("\\")[4] == "robot":   # robot 框架本身要过滤掉
                        self.copy_file_or_dir(path, i)
                    else:
                        # 否则就需要修改目的路径为 pth 文件内的地址
                        i = str(i).replace(i.split("\\")[4], lib_path_ok[1] + "\{}".format(i.split("\\")[4]))
                        self.copy_file_or_dir(path, i)
        print u"所有库文件更新完成！"


if __name__ == "__main__":
    app = UpdateLib()
    app.update_files()
