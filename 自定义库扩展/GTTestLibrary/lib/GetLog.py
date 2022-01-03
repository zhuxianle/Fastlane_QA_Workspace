#coding=utf-8

import os
import adbUtils


class Al:
    def __init__(self, device=""):
        self.device = device

    def _get_android_log(self, log_path):
        """
        :return:清理当前设备缓存log,并且记录当前设备log
        """

        adb = adbUtils.ADB(self.device)
        adb.c_logcat()
        adb.logcat(log_path)

    def analyze_log(self, log_file):
        """
        过滤Exception到log文件夹内
        :param log_file: log的路径
        :return:
        """
        if not os.path.exists(log_file):
            return

        errorId = 0
        go_on_id = 0
        log_file_path = os.path.split(log_file)[0]
        log_filter_name = os.path.split(log_file)[1].split('.')[0]

        log_error_file = log_file_path + '/{}_error.log'.format(log_filter_name)

        with open(log_error_file, 'w') as s:

            with open(log_file) as f:
                for line in f:
                    if 'Exception' in line:
                        go_on_id = 1
                        s.write('#' + '-' * 40 + '\n')
                        s.write(line)
                        errorId = line.split('(')[1].split(')')[0].strip()
                    elif go_on_id == 1:
                        if errorId in line:
                            s.write(line)
                        else:
                            go_on_id = 0

    def main(self, log_path):
        """
        :return: 开启记录log
        """
        return self._get_android_log(log_path)


if __name__ == '__main__':
    pass
