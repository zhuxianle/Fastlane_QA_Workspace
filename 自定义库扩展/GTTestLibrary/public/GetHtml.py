#coding=utf-8

import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def get_now_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def get_html_tr(case_name, img_path, per, device_log, filter_log):
    """
    :param case_name:case名
    :param img_path: case截图地址
    :param per: 性能图表地址列表
    :param device_log: log文件地址
    :param filter_log: 过滤后的文件地址
    :return: html tr部分
    """
    tr = """
    <tr bgcolor="MintCream"  class="gallery cf">
            %(case_name)s
            %(img)s
            %(per)s
            %(log)s
    </tr>
    """

    case_name = '<td style="border:1px solid #ccc">{}</td>'.format(case_name)
    img = '<td style="border:1px solid #ccc"><h><img src="{}" align="absmiddle" width="130" height="200"/></h></td>'.format(img_path)

    per_str = '<td style="border:1px solid #ccc">'
    for i in range(len(per)):
        per_str += '<h><img src="%s" align="absmiddle" width="250" height="200"/></h>' % per[i]
    per_str = per_str + '</td>'

    device_log = '<td style="border:1px solid #ccc"><a href="{}">device_log</a></br></br><a href="{}">device_error_log</a></td>'.format(device_log, filter_log)

    result = {'case_name': case_name, 'img': img, 'per': per_str, 'log': device_log}

    return tr % result


def get_html(log, device, app_info, test_result, result_path):
    """
    :param log: 测试报告报表
    :param device: device信息
    :param app_info: 测试应用信息
    :param test_result: 功能测试报告和日志的位置 (列表)
    :param result_path: 输出文件夹
    :return: 文件保存路径
    """
    result_test_log = test_result[1]
    result_test_report = test_result[0]
    css_style = '''.gallery > td {position: relative;}
        .gallery > td > h >img {
          transition: .1s transform;
          transform: translateZ(1);
        }
        .gallery > td:hover {
          z-index: 1;
        }
        .gallery > td > h > img:hover  {
          transform: scale(2.0, 2.0);
          transition: .3s transform;
        }
    '''

    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
        <title>Test Report</title>
        <style>
        {css_style}
        </style>
    </head>
    <body style="color: black;font-family: Helvetica,sans-serif;">
    <span style="color:green;"><h1>Performance Test Report</h1></span>
    <p><span style="color:blue;">Test End Time: {Time}</p>
    <p><span style="color:blue;">Device Info: {device}</p>
    <p><span style="color:blue;">App Info: {app_info}</p>
    <table>
    </table>
    <div style="position: fixed;right: 0;text-align: center;top: 0;width: 12em;z-index: 1000;">
        <div>
            <a style="background: black none repeat scroll 0 0;color: white;border: 1px solid white;border-bottom-left-radius: 4px;display: block;font-weight: bold;padding: 0.3em 0;"
             href="{result_test_log}">功能测试日志</a>
        </div>
        <div>
            <a style="background: black none repeat scroll 0 0;color: white;border: 1px solid white;border-bottom-left-radius: 4px;display: block;font-weight: bold;padding: 0.3em 0;"
             href="{result_test_report}">功能测试报告</a>
        </div>
    </div>
    <table style="border:1px solid #ccc"
cellpadding="10">
        <tbody>
        <tr bgcolor="MintCream">
            <th>case_name</th>
            <th>case_img</th>
            <th>case_per</th>
            <th>log</th>
        </tr>
            %(tr)s

        </tbody>
    </table>
    </body>
    </html>
    '''.format(css_style=css_style, Time=get_now_time(), device=device, app_info=app_info, result_test_log=result_test_log, result_test_report=result_test_report)
    data = {'tr': log}
    save_html_file = '%s\\Report.html' % result_path
    with open(save_html_file, 'w') as f:
        f.write(template % data)
        f.close()
    return save_html_file


if __name__ == '__main__':
    pass
