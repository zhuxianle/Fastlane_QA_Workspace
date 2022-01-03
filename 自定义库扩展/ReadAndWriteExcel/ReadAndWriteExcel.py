#-*- coding: utf8 -*-

from robot.libraries.BuiltIn import BuiltIn
from robot.utils.asserts import assert_true, assert_equal
from os.path import join
from datetime import date, datetime
from xlrd import open_workbook, xldate_as_tuple
import xlwt, csv
from xlutils.copy import copy
import os, sys, shutil, time


class ReadAndWriteExcel:

    def __init__(self):
        self.FilePath = None
        self.sheetName = None
        self.rb = None

    def confirm_file(self, file_path):
        """
        检查文件是否存在。

        参数：

        file_path:文件地址

        返回: True 或 False
        """
        if os.path.exists(file_path):
            return True
        else:
            return False

    def Set_ExcelPath(self, FilePath):
        """
        设置Excel数据文件的路径。
        必须先设置才能使用后面的关键字。

        参数:
         - FilePath： 文件路径

        例如:
           | Set ExcelPath | F:\\\Test_Data\\\excel.xls |
        """
        self.FilePath = FilePath
        self.rb = open_workbook(self.FilePath, 'r+b')
        print u"准备读取Excel数据文件！ %s" % self.FilePath

    def delete_case_dir(self, file_path):
        """
        检查指定目录下的以【case名称】命名的文件夹是否存在.有就删除。

        参数：

        file_path:父文件夹的路径

        返回: True 或 False
        """
        case_name = self._get_case_name()
        dir_path = file_path + "\\" + case_name
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            time.sleep(2)
            return True
        else:
            return False

    def CSV_To_XLS(self, File_Path, New_FilePath, match_str=""):
        """
        往csv文件转换成xls文件格式。

        参数:
         - File_Path： 待转换的文件列表（必须为列表）

         - New_FilePath： 新文件保存的目录

         - match_str: 在提供的待转换的文件列表中去匹配文件名包含的字符（只转换文件名匹配的文件）

         根据可采集的数据类型,match_str 可以取 【FPS、Pcp(cpu)、Pjif(cpu时间片)、Pnet、Pr(私有内存pri)、Ps(内存pss)】

         返回：转换后的新文件路径列表。
         """
        assert_true(type(File_Path) == list, u"首个参数必须为list类型！")
        case_name = self._get_case_name()

        if not os.path.exists(New_FilePath):
            if not os.path.exists(os.path.dirname(os.path.abspath(New_FilePath))):
                os.mkdir(os.path.dirname(os.path.abspath(New_FilePath)))
            os.mkdir(New_FilePath)

        File_Path_List = []
        if match_str != "":
            for x in range(len(File_Path)):
                if str(match_str) in File_Path[x]:
                    File_Path_List.append(File_Path[x])
        else:
            File_Path_List = File_Path

        return_filename = []

        for count in range(len(File_Path_List)):
            myexcel = xlwt.Workbook(encoding='utf-8')
            mysheet = myexcel.add_sheet("sheet1")
            csvfile = open(File_Path_List[count], "rb")
            reader = csv.reader(csvfile)
            l = 0
            for line in reader:
                r = 0
                # print line
                for i in line:
                    #这里分别处理了数据的类型。数字字符串、带%的数字字符串、字符串
                    if i.isdigit():
                        mysheet.write(l, r, int(i))
                    elif i.endswith("%"):
                        i = i.strip("%")
                        mysheet.write(l, r, float(i))
                    else:
                        mysheet.write(l, r, i)
                    r = r + 1
                l = l + 1

            temp_path = New_FilePath + "\\" + case_name
            #检查case目录文件夹是否存在
            if not self.confirm_file(temp_path):
                os.mkdir(temp_path)

            excel_filename = New_FilePath + "\\" + case_name + "\\{}_{}_{}.xls".format(case_name, match_str, count)
            myexcel.save(excel_filename)
            return_filename.append(excel_filename)

        return return_filename

    #写数据
    def Write_Excel(self, sheetName, rowIndex, lineIndex, content):
        """
        往文件中特定单元格写入数据（暂时有点问题，写入数据后Excel文件无法打开，可能修改了文件格式，但是文件没损坏还可以正常读写数据）。
        必须先设置才能使用后面的关键字。

        参数:
         - FilePath： 文件路径
         - rowIndex： 要往第几行写入数据
         - colIndex： 要往第几列写入数据
         - content： 要写入的数据内容

        例如:
           | Write Excel | Sheet1 | 3 | 2 | 123 |
        """
        rbook = open_workbook(self.FilePath, 'w')
        wb = copy(rbook)
        sheetIndex = rbook.sheet_names().index(sheetName)
        wb.get_sheet(int(sheetIndex)).write(int(rowIndex) - 1, int(lineIndex) - 1, content)
        wb.save(self.FilePath)
        print u"写入数据成功！"

    # 获取某一行数据
    def Get_RowIndexData_By_SheetName(self, sheetName, rowIndex):
        """
        获取某一行的数据，返回一个列表，列表内存储该行内每个单元格的数据。
        必须先设置文件路径才能使用该关键字。

        参数:
         - sheetName： Excel文件内的sheet名称
         - rowIndex： 要获取第几行的数据

        例如:
           | ${data}= | Get RowIndexData By SheetName | Sheet1 | 2 |
        """
        return self.rb.sheet_by_name(sheetName).row_values(int(rowIndex) - 1)

    def Get_Range_RowIndexData_By_SheetName(self, sheetName, rowIndex, min_row, max_row):
        """
        获取某一行中的一定范围内的数据
        - sheetName： Excel文件内的sheet名称

         - rowIndex： 要获取第几行的数据

         - min_row: 范围开始点

         - max_row： 范围结束点

         返回：特定范围内的数据列表
        """
        row_data = self.Get_RowIndexData_By_SheetName(sheetName, rowIndex)
        data = []
        for i in range(int(min_row)-1, int(max_row)):
            data.append(row_data[i])

        return data

    #获取某一列数据
    def Get_ColIndexData_By_SheetName(self, sheetName, colIndex):
        """
        获取某一列的数据，返回一个列表，列表内存储该列内每个单元格的数据。
        必须先设置文件路径才能使用该关键字。

        参数:
         - sheetName： Excel文件内的sheet名称
         - colIndex： 要获取第几列的数据

        例如:
           | ${data}= | Get ColIndexData By SheetName | Sheet1 | 2 |
        """
        return self.rb.sheet_by_name(sheetName).col_values(int(colIndex) - 1)

    def Get_Range_ColIndexData_By_SheetName(self, sheetName, colIndex, min_row, max_row):
        """
        获取某一列中的一定范围内的数据
        - sheetName： Excel文件内的sheet名称

         - colIndex： 要获取第几列的数据

         - min_row: 范围开始点

         - max_row： 范围结束点

         返回：特定范围内的数据列表
        """
        col_data = self.Get_ColIndexData_By_SheetName(sheetName, colIndex)
        data = []
        for i in range(int(min_row)-1, int(max_row)):
            data.append(col_data[i])

        return data

    #获取总行数
    def Get_RowCount_By_SheetName(self, sheetName):
        """
        获取某个sheet的总行数，返回一个整型数据。
        必须先设置文件路径才能使用该关键字。

        参数:
         - sheetName： Excel文件内的sheet名称

        例如:
           | ${count}= | Get RowCount By SheetName | Sheet1 |
        """
        return int(self.rb.sheet_by_name(sheetName).nrows)

    # 获取总列数
    def Get_columnCount_By_SheetName(self, sheetName):
        """
        获取某个sheet内的总列数，返回一个整型数据。
        必须先设置文件路径才能使用该关键字。

        参数:
         - sheetName： Excel文件内的sheet名称

        例如:
           | ${count}= | Get ColumnCount By SheetName | Sheet1 |
        """
        return int(self.rb.sheet_by_name(sheetName).ncols)

    def Get_Number_of_Match_cells(self, sheetName, colIndex, match_string):
        """
        获取某个sheet内包含特定单元格内容的个数和参数字典.

        注:参数字典是匹配的单元格所在行,后面的入参列和出参列所组成的字典---字典键值分别为:"In_Parame" "Out_Parame")

        参数:
         - sheetName： Excel文件内的sheet名称
         - colIndex： 要匹配第几列的数据
         - match_string: 待匹配的内容

         例如:
           | ${count} | ${result} | Get Number of Match cells | Sheet1 | 1 | case_test_1 |

           表示获取Excel内工作表Sheel1的第一列内容为'case_test_1' 所在行入参数据和预期结果.'

           所以取值的时候使用 ${result[0]['In_Parame']}  和 ${result[0]['Out_Parame']} 表示字典的第一个入参和出参
        """
        i_list = []
        In_Parame_ColIndex = 0
        Out_Parame_ColIndex = 0
        for irow in range(self.Get_RowCount_By_SheetName(sheetName)):
            d = {}
            if self.rb.sheet_by_name(sheetName).row_values(irow)[int(colIndex) - 1] == match_string:
                # 总列数遍历
                for i in range(self.Get_columnCount_By_SheetName(sheetName)):
                    if u"入参数据" in self.rb.sheet_by_name(sheetName).col_values(i)[0]:
                        In_Parame_ColIndex = i
                    elif u"预期结果" in self.rb.sheet_by_name(sheetName).col_values(i)[0]:
                        Out_Parame_ColIndex = i

                d["In_Parame"] = self.rb.sheet_by_name(sheetName).row_values(irow)[In_Parame_ColIndex]
                d["Out_Parame"] = self.rb.sheet_by_name(sheetName).row_values(irow)[Out_Parame_ColIndex]
                i_list.append(d)
        count_list = len(i_list)
        return count_list, i_list

    # 获取某个单元格的值
    def Get_Cell_By_ColIndex_RowIndex(self, sheetName, rowIndex, colIndex):
        """
        获取某一行某一列中特定单元格内的数据。
        必须先设置文件路径才能使用该关键字。

        参数:
         - sheetName： Excel文件内的sheet名称
         - rowIndex： 要获取第几行的数据
         - colIndex： 要获取第几列的数据

        例如:
           | ${data}= | Get Cell By ColIndex RowIndex | Sheet1 | 2 | 2 |
        """
        cell_type = self.rb.sheet_by_name(sheetName).cell(int(rowIndex) - 1, int(colIndex) - 1).ctype
        if cell_type == 3:     #如果单元格内是  2016/7/19 这样的时间类型则转换
            data_tmp = xldate_as_tuple(self.rb.sheet_by_name(sheetName).cell_value(int(rowIndex) - 1, int(colIndex) - 1), self.rb.datemode)
            data_value = date(*data_tmp[:3]).strftime('%Y/%m/%d')
            return data_value
        else:
            return self.rb.sheet_by_name(sheetName).cell_value(int(rowIndex) - 1, int(colIndex) - 1)

    #获取单元格的数据类型
    def Get_Cell_Type(self, sheetName, rowIndex, colIndex):
        """
        返回特定单元格内的数据类型(ctype : 0 empty,  1 string,  2 number,  3 date,  4 boolean,  5 error)。
        必须先设置文件路径才能使用该关键字。

        参数:
         - sheetName： Excel文件内的sheet名称
         - rowIndex： 第几行
         - colIndex： 第几列

        例如:
           | ${type}= | Get Cell Type | Sheet1 | 3 | 2 |
        """
        return self.rb.sheet_by_name(sheetName).cell(int(rowIndex) - 1, int(colIndex) - 1).ctype

    #解析单元格数据内容
    def Parse_Cell_Content(self, content, split_str=""):
        """
        返回单元格内的参数列表(用来解析入参和出参单元格内的参数)。

        参数：
        - content: 待处理的内容
        - split_str： 提供处理的字符串来切割返回的内容字符串
        :return:
        """
        str_list = content.split(split_str)
        return str_list

    # Private
    def _get_case_name(self):
        variables = BuiltIn().get_variables()
        return variables['${TEST NAME}']


if __name__ == "__main__":
    path = r"E:\02_产品相关\01_QA_SVN项目\新区大平台自动化测试系统\System_Public_Res\Test_Data\API_Test_ExcelData.xlsx"
    app = ReadAndWriteExcel()
    app.Set_ExcelPath(unicode(path, "utf-8"))
    result = app.Get_Number_of_Match_cells("Sheet1", 1, "POST_api_seller_login")
    print result


