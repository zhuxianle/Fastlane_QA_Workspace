#coding=utf-8

from robot.api import logger
from robot.utils.dotdict import DotDict
from robot.libraries.BuiltIn import BuiltIn
from robot.utils.asserts import assert_true
import public.GetFilePath as GetFilePath
import utils.Performance as Performance
import utils.GenerateReports as GenerateReports
import lib.GetLog as GetLog
import lib.adbUtils as adbUtils
import os, datetime, time, tempfile, subprocess


class GTLibrary(object):

    def __init__(self):
        self._result = ""
        adbUtils.ADB().kill_server()

    def connect_ADB_wireless(self, device_ip):
        """
        通过WiFi连接远程无线设备。可用于无线远程连接appium server来进行测试

        参数：

        device_ip: 设备的IP地址。(如：必须确保 设备IP、appium server、脚本客户端 均处于同一个局域网网段)
        """
        value = subprocess.Popen("adb connect %s:5555" % device_ip, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().strip()
        logger.info(u"\t\n%s \t\n" % value)
        assert ("cannot connect" not in value), u"连接设备失败！请检查原因。(可能需要重新启动手机端的 adb 服务)"

        self.device = "%s:5555" % device_ip
        self.ADB = adbUtils.ADB(self.device)

    def sync_time(self):
        """同步本地时间。
        """
        sync_time = datetime.datetime.now().strftime("%Y%m%d.%H%M%S")
        cmd = 'date -s ' + sync_time
        self.ADB.shell(cmd)
        logger.info(u"\t\n已完成手机端和计算机端的时间同步！\t\n")

    def start_gt(self):
        """启动GT。
        """
        cmd = 'am start -W -n com.tencent.wstt.gt/com.tencent.wstt.gt.activity.GTMainActivity'
        self.ADB.shell(cmd)
        logger.info(u"\t\n已成功启动GT！\t\n")

    def set_collect_data(self, appname):
        """设置要采集性能数据的被测App
        """
        cmd = 'am broadcast -a com.tencent.wstt.gt.baseCommand.startTest --es pkgName ' + appname
        self.ADB.shell(cmd)
        time.sleep(1)
        logger.info(u"\t\nApp [%s] 配置设置完成！\t\n" % appname)

    def stop_collect_data(self, save_folder_name, desc):
        """结束采集并保存。每次保存完清空本次缓存测试数据。

        参数:
         - save_folder_name： 为保存目录的名称(暂时还不支持中文名)

         - desc： 对本次手机数据文件的描述

        例如:
           | Stop Collect Data | case1 | case1_desc |
        """
        cmd1 = 'rm -rf /sdcard/GT/GW/* '
        cmd2 = 'am broadcast -a com.tencent.wstt.gt.baseCommand.endTest --es saveFolderName ' + save_folder_name + ' ' + '--es desc ' + desc
        self.ADB.shell(cmd1)
        self.ADB.shell(cmd2)
        logger.info(u"\t\n已经结束采集并保存数据！\t\n")

    def download_data(self, download_path=None):
        """下载数据结果文件到本地计算机。

        默认下载至系统临时目录。

        返回：保存文件的本地路径列表。
        """
        if download_path is not None:
            TEMP_FILE = download_path
        else:
            PATH = lambda p: os.path.abspath(p)
            TEMP_FILE = PATH(tempfile.gettempdir())

        logger.info(u"\t\n开始下载测试结果文件！\t\n")

        cmd = 'pull /sdcard/GT/GW {}'.format(TEMP_FILE)

        data_file1 = TEMP_FILE + "\\com.azt.kaimai8"
        data_file2 = TEMP_FILE + "\\GW\\com.azt.kaimai8"
        GetFilePath.confirm_file(data_file1)
        GetFilePath.confirm_file(data_file2)

        self.ADB.adb(cmd)

        time.sleep(5)
        logger.info(u"\t\n测试结果文件下载完成！\t\n")

        #返回的列表排下序
        if os.path.exists(data_file1):
            return sorted(GetFilePath.all_file_path(data_file1, "csv").values())
        else:
            return sorted(GetFilePath.all_file_path(data_file2, "csv").values())

    def start_or_stop_collect(self, collect_type, status):
        """开始或停止采集性能数据。

        参数:
         - collect_type： 采集数据的类型。主要包括以下：

                | cpu：      | CPU采集 |

                | jif:       | CPU时间片采集 |

                | pss:       | PSS采集(内存) |

                | pri:       | PrivateDirty采集 |

                | net:       | NET采集(网络流量) |

                | fps:       | FPS采集(每秒帧数) |

         - status： 开启或关闭。数字表示（1：表示开启。 0：表示关闭）

        例如:
           | Start Or Stop Collect | cpu | 1 |
        """
        cmd = 'am broadcast -a com.tencent.wstt.gt.baseCommand.sampleData --ei ' + collect_type + ' ' + status
        self.ADB.shell(cmd)
        time.sleep(0.5)
        logger.info(u"\t\n已经完成 [%s] 性能数据的采集设置！\t\n" % collect_type)

    def start_SM_test(self, proc_name):
        """流畅度(SM)的获取。所谓的流畅度其实就是系统界面UI切换的响应速度

        参数:
         - proc_name： 获取被测app的进程名。

        例如:
           | Start SM Test | com.azt.kaimai8 |
        """
        cmd = 'am broadcast -a com.tencent.wstt.gt.plugin.sm.startTest --es procName ' + proc_name
        self.ADB.shell(cmd)
        logger.info(u"\t\n已开启流畅度测试！\t\n")

    def stop_SM_test(self):
        """停止流畅度测试。
        """
        cmd1 = 'am broadcast -a com.tencent.wstt.gt.plugin.sm.endTest'
        self.ADB.shell(cmd1)
        cmd2 = 'am broadcast -a com.tencent.wstt.gt.plugin.sm.resume'
        self.ADB.shell(cmd2)
        cmd3 = 'am broadcast -a com.tencent.wstt.gt.plugin.sm.modify'
        self.ADB.shell(cmd3)
        logger.info(u"\t\n已停止流畅度测试！\t\n")

    def start_battery_test(self, refresh_rate=250, brightness=100):
        """APP耗电测试（对应耗电测试插件）,主要关注的指标包括：电流(I)、电压(U)、电量(P--Power)、温度(T--Temp)

        参数:
        - refresh_rate： 刷新率(ms)。

         - brightness： 屏幕亮度。

        例如:
           | Start Battery Test | 250 | 100 |
        """
        cmd = 'am broadcast -a com.tencent.wstt.gt.plugin.battery.startTest --ei refreshRate ' + refresh_rate + ' ' + '--ei brightness ' + brightness + ' ' \
              + '--ez I true --ez U true --ez T true --ez P true'
        self.ADB.shell(cmd)
        logger.info(u"\t\n已开启耗电量测试！\t\n")

    def stop_battery_test(self):
        """停止耗电量测试。
        """
        cmd = 'am broadcast -a com.tencent.wstt.gt.plugin.battery.endTest'
        self.ADB.shell(cmd)
        logger.info(u"\t\n已停止耗电量测试！\t\n")

    def start_memfill_test(self, size):
        """APP内存填充测试（对应内存填充插件）

        参数:
         - size： 要填充的内存大小。

        例如:
           | Start Memfill Test | 200 |
        """
        cmd = 'am broadcast -a  com.tencent.wstt.gt.plugin.memfill.fill --ei size ' + size
        self.ADB.shell(cmd)
        logger.info(u"\t\n已开启内存填充测试！\t\n")

    def free_mem(self):
        """内存释放(针对于内存填充测试)。
        """
        cmd = 'am broadcast -a com.tencent.wstt.gt.plugin.memfill.free'
        self.ADB.shell(cmd)
        logger.info(u"\t\n内存释放完成，已结束内存填充测试！\t\n")

    def start_app_tcpdump(self, filepath):
        """开启广播抓包

        参数:
         - filepath： 抓包获取的数据文件保存的路径。

        例如:
           | Start App Tcpdump | /sdcard/GT/Tcpdump/Capture/aaa.pcap |
        """
        cmd = 'am broadcast -a com.tencent.wstt.gt.plugin.tcpdump.startTest --es filepath ' + filepath + ' ' + '--es param "-p -s 0 -vv -w"'
        self.ADB.shell(cmd)
        logger.info(u"\t\n已开启广播抓包！\t\n")

    def stop_app_tcpdump(self):
        """结束抓包
        """
        cmd = 'am broadcast -a com.tencent.wstt.gt.plugin.tcpdump.endTest'
        self.ADB.shell(cmd)
        logger.info(u"\t\n已结束广播抓包！\t\n")

    def close_gt(self):
        """关闭GT。
        """
        cmd = 'am broadcast -a com.tencent.wstt.gt.baseCommand.exitGT'
        self.ADB.shell(cmd)
        logger.info(u"\t\n已成功关闭GT！\t\n")

    def save_android_log(self, file_path):
        """开始记录设备日志，保存至图片目录。

        参数：

        file_path：当前case的设备日志保存的目录
        """
        GetFilePath.create_dir(file_path)

        case_name = self._get_case_name()
        # case_name = u"Case_用户登录"
        temp_path = file_path + "\\" + case_name
        GetFilePath.create_dir(temp_path)

        self._save_android_log(temp_path, case_name)

    def marker_performance_data(self, param1, param2, file_path, match_str):
        """生成性能数据，保存至图片目录。

        参数：

        param1 - param2: 两个性能参数列表 (必须是列表，可以取空)

        file_path：性能图表保存的目录

        match_str：生成性能图表的类型 (可选 Mem、CPU、NET、FPS、JIF)
        """
        GetFilePath.create_dir(file_path)

        case_name = self._get_case_name()
        # case_name = u"Case_用户登录"
        temp_path = file_path + "\\" + case_name
        GetFilePath.create_dir(temp_path)
        log_file = temp_path + '/{}.log'.format(case_name)

        GetLog.Al().analyze_log(log_file)  #保存并过滤设备日志log
        save_path = temp_path + "\\{}.png".format(match_str)
        Performance.data_marker(param1, param2, save_path, match_str=match_str)

    def marker_performance_report(self, per_path, all_result_path, extra_param):
        """生成性能测试报告，保存至测试报告目录。

        参数：

        per_path：性能图表文件目录。

        all_result_path：性能测试报告保存的目录。

        extra_param：额外参数，由执行测试case时传入。(必须是robot框架定义的字典类型)

        备注：额外参数字典中必须包含的item有：Device_Name、Platform_Name、Platform_Version、Result_List(功能测试的日志和报告文件路径列表)
        """
        assert_true(type(extra_param) == DotDict, u"额外参数必须为dict字典类型！")

        GetFilePath.create_dir(all_result_path)

        device_info = '[ Device_Name：' + str(extra_param["Device_Name"]) + "、" + "Platform_Name：" + str(extra_param["Platform_Name"]) + "、" \
                      + "Platform_Version：" + str(extra_param["Platform_Version"]) + " ]"
        app_info = '[ App：' + str(extra_param["App_Package"]) + " ]"

        test_result = extra_param["Result_List"]  #功能测试报告和日志的列表
        #拷贝功能测试报告和日志
        GetFilePath.create_dir(all_result_path + "\\robot_report")
        GetFilePath.copy_files(test_result, all_result_path + "\\robot_report")

        # 修改功能测试报告和日志内容
        source_content = '<div id="report-or-log-link2"><a href="#">'
        dst_content = '<div id="report-or-log-link2"><a href="../Report.html">'

        for file in GetFilePath.all_file_path(all_result_path + "\\robot_report", "html").values():
            GetFilePath.replace_file_content(file, source_content, dst_content)

        GenerateReports.Gr(all_result_path, extra_param["Device_Name"]).get_report_main(per_path, device_info, app_info, GetFilePath.all_file_path(all_result_path
                                                                                                                                                   + "\\robot_report", "html").values())

    # Private
    def _get_case_name(self):
        variables = BuiltIn().get_variables()
        return variables['${TEST NAME}']

    def _save_android_log(self, log_file_path, filename):
        """
        :return:清理当前设备缓存log,并且记录当前设备log
        """
        android_log = GetLog.Al(self.device)
        log_file = log_file_path + '/{}.log'.format(filename)
        android_log.main(log_file)
        return log_file

    def _get_device_list(self):
        """
        :return: 返回Android设备列表
        """
        android_devices_list = []
        for device in self.cmd('adb devices').stdout.readlines():
            if 'device' in device and 'devices' not in device:
                device = device.split('\t')[0]
                android_devices_list.append(device)

        return android_devices_list

if __name__ == "__main__":
    a = GTLibrary()
    a.sync_time()