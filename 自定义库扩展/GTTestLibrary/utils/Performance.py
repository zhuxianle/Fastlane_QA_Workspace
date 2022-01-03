#coding=utf-8


def data_marker(param1, param2, path, match_str):
    """
    :param param1-param4: 4个性能参数列表。没有则取空即可。
    :param path: 存储的文件路径
    :param match_str：表示选择要生成的性能类型图(Mem、CPU、JIF、NET、FPS)
    :return:
    """
    import matplotlib

    matplotlib.use('Agg')
    import pylab as pl

    if match_str == "Mem":
        pl.title('performance')
        pl.xlabel('second')
        pl.ylabel('MB')

        #取M 为单位,所以每个列表的值除以1024
        param1 = [float(i/1024) for i in param1]
        param2 = [float(i/1024) for i in param2]

        pl.plot(param1, color="red", linewidth=2.5, linestyle="-", label="PSS_0")
        pl.plot(param2, color="magenta", linewidth=2.5, linestyle="-", label="Pri_0")

        pl.legend(loc='upper left')
        pl.xlim(0.0, len(param1))
        pl.ylim(0.0, 200.0)
        pl.savefig(path)
        # U.Logging.debug('Report:%s' % path)
        # pl.show() #调出GUI实时查看
        pl.close()  # 必须关闭,不然值会在内存中不销毁

    elif match_str == "CPU":
        pl.title('performance')
        pl.xlabel('second')
        pl.ylabel('%')

        pl.plot(param1, color="red", linewidth=2.5, linestyle="-", label="Pcp_0")

        pl.legend(loc='upper left')
        pl.xlim(0.0, len(param1))
        pl.ylim(0.0, 100.0)
        pl.savefig(path)
        pl.close()
    elif match_str == "JIF":
        pl.title('performance')
        pl.xlabel('second')
        pl.ylabel('')

        pl.plot(param1, color="red", linewidth=2.5, linestyle="-", label="Pjif_0")

        pl.legend(loc='upper left')
        pl.xlim(0.0, len(param1))
        pl.ylim(0.0, 5000.0)
        pl.savefig(path)
        pl.close()
    elif match_str == "NET":
        pl.title('performance')
        pl.xlabel('second')
        pl.ylabel('MB')

        #取M 为单位,所以每个列表的值除以1024
        param1 = [float(i/1024) for i in param1]
        param2 = [float(i/1024) for i in param2]
        pl.plot(param1, color="red", linewidth=2.5, linestyle="-", label="NET-Transmitted")
        pl.plot(param2, color="blue", linewidth=2.5, linestyle="-", label="NET-Received")

        pl.legend(loc='upper left')
        pl.xlim(0.0, len(param1))
        pl.ylim(0.0, 20.0)
        pl.savefig(path)
        pl.close()
    elif match_str == "FPS":
        #FPS和 SM(流畅度) 一起合并了
        pl.title('performance')
        pl.xlabel('second')
        pl.ylabel('Frame Per Second(Hz)')

        pl.plot(param1, color="red", linewidth=2.5, linestyle="-", label="FPS")
        pl.plot(param2, color="blue", linewidth=2.5, linestyle="-", label="SM")

        pl.legend(loc='upper left')
        pl.xlim(0.0, len(param1))
        pl.ylim(0.0, 100.0)
        pl.savefig(path)
        pl.close()
    else:
        raise TypeError(u"匹配类型错误！Mem、CPU、NET、FPS、JIF")


if __name__ == '__main__':
    data_marker()
