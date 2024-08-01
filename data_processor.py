import collections
import pandas as pd
import re

class DataProcessor:

    # 初始化Log信息
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = self.get_last_n_lines(100) # 读取文件最后1000行,并分割文本
        
    # 获取文件最后n行
    def get_last_n_lines(self, n):
        with open(self.file_path, 'r') as file:
            # 使用collections.deque实现双端队列，从右边添加元素，从左边弹出元素，存储最后n行
            lines = collections.deque(file, n)
            # 返回解析后列表
            return self.split_lines(list(lines))

    # 利用正则表达式分割文本
    def split_lines(self, lines=None):
        # Define the regex pattern
        regex = r'^(\d+):([a-zA-Z ]+):(.+)$' # 每一行必须以数字开头，然后是一个冒号，接着是一个或多个字母或空格，再一个冒号，最后是任意字符
        # Parse each line
        parsed_lines = []
        # Print each line
        for line in lines:
            match = re.match(regex, line)
            if match:
                if match.group(2) == 'PAP':
                    parsed_lines.append(list(match.groups()))

        # Return parsed lines
        return parsed_lines

    # 字符串转数字
    def str_to_num(self, s):
        try:
            return int(s)   # python3中int()函数可以直接处理字符串,且不会溢出
        except ValueError:
            return float(s)

    # 将解析后的列表转换为DataFrame
    def to_dataframe(self, parsed_lines):
            # Convert parsed lines to DataFrame
            df = pd.DataFrame(parsed_lines, columns=['Number', 'Module', 'Text'])
            return df

    # 将DataFrame转换为list
    def to_list(self, df):
        return df.values.tolist()

# 示例使用
if __name__ == "__main__":
    file_path = "d:/MyProject/printer_check/printer_log.txt"
    data_processor = DataProcessor(file_path)
    for i in data_processor.lines:
        print(i)