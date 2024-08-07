import collections
import pandas as pd
import re
from printer_data import PrinterData

class DataProcessor:

    def __init__(self, file_path, printer_data, n_lines=1000):
        """初始化Log信息"""
        self.file_path = file_path
        self.parsed_massege = {} # 存储各页信息
        self.printer_data = printer_data # 打印机配置信息
        self.lines = self.get_last_n_lines(n_lines) # 读取文件最后n行,并分割文本
        self.pap_logs = self.split_PAP_lines() # 获取纸搬送信息,传参时，这里可能无法传递所有log信息

    def get_last_n_lines(self, n):
        """获取文件最后n行"""
        with open(self.file_path, 'r') as file:
            # 使用collections.deque实现双端队列，从右边添加元素，从左边弹出元素，存储最后n行
            lines = collections.deque(file, n)
            # 返回解析后列表
            return list(lines)

    def split_PAP_lines(self):
        """利用正则表达式分割搬送文本,并提取sheet信息"""
        # Define the regex pattern
        regex = r'^(\d+):([a-zA-Z ]+):(.+)$' # 每一行必须以数字开头，然后是一个冒号，接着是一个或多个字母或空格，再一个冒号，最后是任意字符
        # Define the regex pattern
        regex1 = self.printer_data.paper_info['1']
        regex2 = self.printer_data.paper_info['2']
        regex3 = self.printer_data.paper_info['3']
        regex4 = self.printer_data.paper_info['4']
        # Parse each line
        parsed_lines = []
        parsed_paper = []
        # define flag
        flag = 0
        num = 0
        pap_start = 0
        # Print each line
        for line in self.lines:
            match = re.match(regex, line)
            if match:
                if regex1 in match.group(3):
                    flag = 1
                    pap_start = 1
                    continue
                if flag == 1:
                    match1 = re.match(regex2, match.group(3))
                    if match1:
                        parsed_paper.append(match.group(3))
                        flag = 2
                        continue
                if flag == 2:
                    match2 = re.match(regex3, match.group(3))
                    if match2:
                        parsed_paper.append(match.group(3))
                        flag = 3
                        continue
                if flag == 3:
                    match3 = re.match(regex4, match.group(3))
                    if match3:
                        parsed_paper.append(match.group(3))
                        flag = 0
                        self.parsed_massege[num] = parsed_paper
                        parsed_paper = []
                        num += 1
                        continue
                # 从检测到打印管理下发任务再开始载入纸信息
                if match.group(2) == 'PAP' and pap_start == 1:
                    parsed_lines.append(list(match.groups()))
                    # print(list(match.groups()))

        # Return parsed lines
        return parsed_lines

    def str_to_num(self, s):
        """字符串转数字"""
        try:
            return int(s)   # python3中int()函数可以直接处理字符串,且不会溢出
        except ValueError:
            return float(s)

    def to_dataframe(self, parsed_lines):
        """将解析后的列表转换为DataFrame"""
        # Convert parsed lines to DataFrame
        df = pd.DataFrame(parsed_lines, columns=['Number', 'Module', 'Text'])
        return df

    def to_list(self, df):
        """将DataFrame转换为list"""
        return df.values.tolist()

# 示例使用
if __name__ == "__main__":
    file_path = "d:/MyProject/printer_check/printer_log.txt"
    printer_data = PrinterData('printer_config.json')
    data_processor = DataProcessor(file_path, printer_data)
    for i in data_processor.pap_logs:
        print(i)

    # 解析第三部分文本
    for i in data_processor.parsed_massege:
        print(data_processor.parsed_massege[i])