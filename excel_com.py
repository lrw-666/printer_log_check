import pandas as pd
import re
import xlsxwriter

# 该类用于进行Excel文件的读写操作
class ExcelHandler:

    def __init__(self, file_path, data_processor=None, paper_controller=None):
        """初始化工作簿"""
        self.file_path = file_path  # file path of the excel file
        self.workbook = xlsxwriter.Workbook(self.file_path)  # create a new workbook
        self.worksheet = None  # wait a  worksheet
        self.data_processor = data_processor  # 获取打印机下发的任务信息
        self.paper_controller = paper_controller  # 获取已处理后的信息

    def get_worksheet(self, sheet_name):
        """获取工作表"""
        for worksheet in self.workbook.worksheets():
            if worksheet.name == sheet_name:    # 如果工作表已经存在，则删除原有的工作表
                self.workbook.remove_worksheet(worksheet)
                break
        
        self.worksheet = self.workbook.add_worksheet(sheet_name) # 重新创建一个空的工作表

    def write_header(self, header, column_widths=None):
        """写入表头并设置列宽"""
        if column_widths is None:
            column_widths = []
        center_format = self.workbook.add_format({'align': 'center', 'valign': 'vcenter'}) # 创建一个居中格式
        # 写入表头
        self.worksheet.write_row(0, 0, header, center_format)
        # 设置列宽
        for col_idx, width in enumerate(column_widths):
            self.worksheet.set_column(col_idx, col_idx, width)

    def merge_cells(self, start_row, start_col, end_row, end_col, cell_format=None):
        """合并单元格:从第start_row行、第start_col列开始;到第end_row行、第end_col列结束"""
        self.worksheet.merge_range(start_row, start_col, end_row, end_col, '', cell_format)# 注：xlsxwriter的行索引从0开始

    def write_data_to_excel(self, data, start_row=0, start_col=0):
        """将数据写入到指定的Excel工作表中"""
        center_format = self.workbook.add_format({'align': 'center', 'valign': 'vcenter'}) # 创建一个居中格式
        for row_idx, row_data in enumerate(data, start=start_row): # 遍历每一行数据:data (list of list)-要写入的数据，每个子列表代表一行数据
            self.worksheet.write_row(row_idx, start_col, row_data, center_format)

    def read_excel_data(self, sheet_name, start_row, end_row, start_col, end_col): # 读取Excel文件、选择工作表、指定起始行、结束行、起始列、结束列
        """读取工作簿数据"""
        data = pd.read_excel(self.file_path, sheet_name=sheet_name,
                             skiprows=start_row - 1, nrows=end_row - start_row + 1,
                             usecols=list(range(start_col - 1, end_col)))
        return data

    def get_sheet_names(self):
        """获取工作簿的sheet名称"""
        return self.workbook.sheetnames

    def get_sheet_data(self, sheet_name):
        """获取工作簿的指定sheet数据"""
        data = pd.read_excel(self.file_path, sheet_name=sheet_name)
        return data

    def get_sheet_data_by_regex(self, sheet_name, regex):
        """获取工作簿的指定sheet数据,通过正则表达式匹配"""
        data = pd.read_excel(self.file_path, sheet_name=sheet_name)
        data = data[data.apply(lambda x: any(re.search(regex, str(x[col])) for col in data.columns), axis=1)]
        return data

    def save_task_massage(self):
        """保存打印机下发的任务结果,写入task_massage页面"""
        if self.data_processor is not None:
            self.get_worksheet("task_massage")
            num = 0
            parsed_list = []
            for paper_info in self.data_processor.parsed_massege:
                parsed_item = self.paper_controller.parse_data(self.data_processor.parsed_massege[paper_info])
                if num == 0:
                    parsed_list.append(list(parsed_item.keys()))
                num += 1
                parsed_list.append([])
                parsed_list.append(list(parsed_item.values()))
            parsed_list.append([])
            parsed_list.append(['共' + str(num) + '页'])
            self.write_data_to_excel(parsed_list, start_row=1)

    def save_pap_logs(self):
        """保存PAP日志,写入PAP_Logs页面"""
        if self.data_processor is not None:
            self.get_worksheet("PAP_Logs")
            header = ['Time', 'PAP', 'Logs']
            column_widths = [10, 10, 50]
            self.write_header(header, column_widths)
            self.write_data_to_excel(self.data_processor.split_PAP_lines(), start_row=1)

    def save_paper_n(self):
        """保存已处理的纸张,分别写入paper_n页面"""
        if self.paper_controller is not None:
            for i in range(self.paper_controller.paper_count):
                # 创建一个新的工作表
                self.get_worksheet("paper_" + str(i))
                # 获取纸对象
                paper = self.paper_controller.papers[i]
                # 写入paper基本信息:占一二两行
                header = ['Id', 'Speed', 'Ftray', 'Etray', 'Length', 'Width', 'Thickness', 'Page_num', 'Subscan', 'Trans', \
                           'Tray1_space', 'Manual_space', 'Tray1_release_time', 'Manual_release_time', 'Actual_length']
                column_widths = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 20, 20, 15]
                self.write_header(header, column_widths)
                paper_data = [paper.id, paper.speed, paper.ftray, paper.etray, paper.length, paper.width, paper.thickness, \
                              paper.page_num, paper.subscan, paper.trans, paper.tray1_space, paper.manual_space, \
                              paper.tray1_release_time, paper.manual_release_time, paper.actual_length]
                self.write_data_to_excel([paper_data], start_row=1)
                # 计算正常系日志所需行数
                logs_num = len(paper.normal_logs) + 1
                # 格式化表格
                rowx = 2
                for j in range(logs_num):
                    self.merge_cells(rowx+j, 2, rowx+j, 6)
                # 写入正常系日志信息：
                logs_data = [['', '', '正常系Log']] + list(paper.normal_logs.values())
                self.write_data_to_excel(logs_data, start_row=rowx)
                # 计算异常系日志所需行数
                logs_num = len(paper.abnormal_logs) + 1
                # 格式化表格
                rowx = 2
                for j in range(logs_num):
                    self.merge_cells(rowx+j, 10, rowx+j, 12)
                # 写入异常系日志信息：
                logs_data = [['', '', '异常系Log']] + list(paper.abnormal_logs.values())
                self.write_data_to_excel(logs_data, start_row=rowx, start_col=8)
                # 计算搬送时序日志所需行数
                logs_num = len(paper.trajectory_map) + 1
                # 格式化表格
                rowx = 12
                for j in range(logs_num):
                    self.merge_cells(rowx+j, 8, rowx+j, 10)
                # 写入异常系日志信息：
                road_path = [[s] for s in list(paper.trajectory_map.keys())] # 路径列表
                logs_data = [['搬送路径']] + road_path
                self.write_data_to_excel(logs_data, start_row=rowx, start_col=8)
                logs_data = [['理论时间', '实际时间', '误差']] + list(paper.trajectory_map.values())
                self.write_data_to_excel(logs_data, start_row=rowx, start_col=11)

    def close(self):
        """关闭工作簿"""
        self.workbook.close()

# 示例使用
if __name__ == "__main__":
    excel_handler = ExcelHandler('C:/Users/PANTUM/Desktop/log_parsed.xlsx')
    excel_handler.get_worksheet('Text1')
    header = ['Name', 'Age', 'City']
    column_widths = [15, 10, 15]
    excel_handler.write_header(header, column_widths)
    data = [
        ['Alice', 30, 'New York'],
        ['Bob', 25, 'Los Angeles']
    ]
    excel_handler.write_data_to_excel(data, start_row=1)
    excel_handler.close()

    # 读取数据
    # read_data = excel_handler.read_excel_data('Text1', start_row=2, end_row=3, start_col=1, end_col=3)
    # print(read_data)

    # 通过正则表达式匹配筛选数据
    regex = r'\bNew York\b'
    filtered_data = excel_handler.get_sheet_data_by_regex('Text1', regex)
    print(filtered_data) # 输出：[['Alice', 30, 'New York']]（pandas.read_excel函数默认会将第一行作为表头（列名））