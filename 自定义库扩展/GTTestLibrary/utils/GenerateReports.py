#coding=utf-8

import os
import GTTestLibrary.lib.adbUtils as adbUtils
import GTTestLibrary.public.GetFilePath as GetFilePath
import GTTestLibrary.public.GetHtml as GetHtml


class Gr:

    def __init__(self, all_result_path, device):
        """
        :param all_result_path: 性能测试报告保存的目录
        :param device: 设备名
        """
        self.all_result_path = all_result_path
        self.device = device
        self.adb = adbUtils.ADB(self.device)

    def device_info(self):
        """
        用于生成测试报告的device的信息
        :return: 设备名,磁盘状态,wifi名称
        """
        return 'device_name:' + str(self.adb.get_device_name()), 'disk:' + str(self.adb.get_disk()), \
               'wifi_name:' + str(self.adb.wifi_name()), 'system_version:' + str(self.adb.get_android_version()), \
               'resolution:' + str(self.adb.get_screen_resolution())

    def app_info(self, package_name):
        """
        获取应用包名和版本号
        :return:
        """
        package_name_version = self.adb.specifies_app_version_name(
            package_name)
        return package_name, package_name_version

    def get_report_main(self, per_path, device_info, app_info, test_result):
        """
        生成测试报告主函数
        :return:
        """
        #目录名其实就是case名
        case_name_lst = os.listdir(per_path)
        per_lst = []
        for i in range(len(GetFilePath.all_dir_path(per_path))):
            case_img_path = per_path + "/" + case_name_lst[i] + "/" + case_name_lst[i] + ".jpg"
            case_log_path = per_path + "/" + case_name_lst[i] + "/" + case_name_lst[i] + ".log"
            case_error_log_path = per_path + "/" + case_name_lst[i] + "/" + case_name_lst[i] + "_error.log"
            per = GetFilePath.all_file_path(GetFilePath.all_dir_path(per_path)[i], "png").values()

            per_lst.append(
                GetHtml.get_html_tr(case_name_lst[i], case_img_path,
                        per,
                        case_log_path,
                        case_error_log_path))

        GetHtml.get_html(''.join(per_lst), device_info, app_info, test_result, self.all_result_path)


if __name__ == '__main__':
    pass