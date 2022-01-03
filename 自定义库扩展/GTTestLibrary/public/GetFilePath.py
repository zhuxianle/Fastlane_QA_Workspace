#coding=utf-8

import os, shutil, time
import fileinput


def all_file_path(root_directory, extension_name):
    """
    :return: 遍历文件目录
    """
    file_dic = {}
    for parent, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if 'filter' not in filename:
                if filename.endswith(extension_name):
                    path = os.path.join(parent, filename).replace('\\', '/')
                    file_dic[filename] = path
    return file_dic


def all_dir_path(root_directory):
    """
    :return: 遍历目录
    """
    file_dic = []
    for parent, dirnames, filenames in os.walk(root_directory):
        for dir in dirnames:
            path = os.path.join(parent, dir).replace('\\', '/')
        # path = os.path.join(parent, filename).replace('\\', '/')
            file_dic.append(path)
    return file_dic


def confirm_file(file_path):
    """
    检查文件是否存在.有就删除。
    :param file_path:文件地址
    :return: True 或 False
    """
    if os.path.exists(file_path):
        # os.remove(file_path)
        shutil.rmtree(file_path)
        time.sleep(2)
        return True
    else:
        return False


def create_dir(file_path):
    """
    创建文件夹。
    :param file_path:文件目录
    :return:
    """
    if not os.path.exists(file_path):
        if not os.path.exists(os.path.dirname(os.path.abspath(file_path))):
            os.mkdir(os.path.dirname(os.path.abspath(file_path)))
        os.mkdir(file_path)


def copy_files(file_lst, file_path):
    """
    拷贝文件
    :param file_lst: 待拷贝的文件列表
    :param file_path: 目的文件夹
    :return:
    """
    for file in file_lst:
        shutil.copy(file, file_path)


def replace_file_content(file, source_content, dst_content):
    """
    替换文件内容
    :param file: 要替换的文件
    :param source_content: 源内容
    :param dst_content: 目的内容，也就是替换后的内容
    :return:
    """
    for line in fileinput.input(files=file, inplace=1):
        line = line.replace(source_content, dst_content)
        print line


if __name__ == "__main__":
    pass
