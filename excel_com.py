import pandas as pd
import re
import xlsxwriter

# 该类用于进行Excel文件的读写操作
class ExcelHandler:
    
    # 初始化工作簿
    def __init__(self, file_path):
        self.file_path = file_path  # file path of the excel file
        self.workbook = xlsxwriter.Workbook(self.file_path)  # create a new workbook
        self.worksheet = None  # wait a  worksheet

    # 获取工作表
    def get_worksheet(self, sheet_name):
        # 如果工作表已经存在，则删除原有的工作表
        for worksheet in self.workbook.worksheets():
            if worksheet.name == sheet_name:
                self.workbook.remove_worksheet(worksheet)
                break
        # 重新创建一个空的工作表
        self.worksheet = self.workbook.add_worksheet(sheet_name)
    
    # 写入表头并设置列宽
    def write_header(self, header, column_widths=None):
        if column_widths is None:
            column_widths = [10, 10, 50]
        # 写入表头
        self.worksheet.write_row(0, 0, header)
        # 设置列宽
        for col_idx, width in enumerate(column_widths):
            self.worksheet.set_column(col_idx, col_idx, width)

    # 将数据写入到指定的Excel工作表中:data (list of list)- 要写入的数据，每个子列表代表一行数据。
    def write_data_to_excel(self, data, start_row=0, start_col=0):
        # 写入数据
        for row_idx, row_data in enumerate(data, start=start_row): # 遍历每一行数据
            self.worksheet.write_row(row_idx, start_col, row_data)

    # 读取工作簿数据：读取Excel文件、选择工作表、指定起始行、结束行、起始列、结束列
    def read_excel_data(self, sheet_name, start_row, end_row, start_col, end_col):
        data = pd.read_excel(self.file_path, sheet_name=sheet_name,
                             skiprows=start_row - 1, nrows=end_row - start_row + 1,
                             usecols=list(range(start_col - 1, end_col)))
        return data

    # 获取工作簿的sheet名称
    def get_sheet_names(self):
        return self.workbook.sheetnames

    # 获取工作簿的指定sheet数据
    def get_sheet_data(self, sheet_name):
        data = pd.read_excel(self.file_path, sheet_name=sheet_name)
        return data

    # 获取工作簿的指定sheet数据，通过正则表达式匹配
    def get_sheet_data_by_regex(self, sheet_name, regex):
        data = pd.read_excel(self.file_path, sheet_name=sheet_name)
        data = data[data.apply(lambda x: any(re.search(regex, str(x[col])) for col in data.columns), axis=1)]
        return data

    # 关闭工作簿
    def close(self):
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