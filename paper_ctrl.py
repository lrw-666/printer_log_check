import re  # 导入正则表达式模块
from paper import Paper  # 导入Paper类
from printer_data import PrinterData  # 导入PrinterData类
from data_processor import DataProcessor

class PaperController:
    def __init__(self, printer_data=None, data_processor=None):
        self.papers = []  # 存储所有纸张对象
        self.paper_count = 0  # 纸张数量
        self.printerData = printer_data  # 打印机配置信息
        self.dataProcessor = data_processor  # 打印数据

    def add_paper(self):
        """根据打印管理的信息，添加纸张对象"""
        for paper_info in self.dataProcessor.parsed_massege:
            # print(self.dataProcessor.parsed_massege[paper_info])
            parsed_item = self.parse_data(self.dataProcessor.parsed_massege[paper_info])
            paper = Paper(id=parsed_item['id'], speed=parsed_item['speed'], ftray=parsed_item['ftray'], etray=parsed_item['etray'], \
                          length=parsed_item['length'], width=parsed_item['width'], thickness=parsed_item['thick'])
            self.papers.append(paper)
            self.paper_count += 1
            print("添加纸张:", paper)
        print("纸张数量:", self.paper_count)

    def parse_data(self, data):
        """解析打印管理数据"""
        parsed_item = {}
        for item in data:
            pairs = item.split()
            for pair in pairs:
                key, value = pair.split(':')
                parsed_item[key] = value

        return parsed_item

    def allocate_PAP_info(self):
        """分配纸搬送log信息"""
        nm_num = int(self.printerData.single_logs['key_node_number'])
        abnm_num = int(self.printerData.jam_logs['key_node_number'])
        # 遍历所有纸张，分配打印log信息
        for paper in self.papers:
            for i in range(1, nm_num+1):
                for log in self.dataProcessor.pap_logs:
                    remove_flag = False
                    # 正常系log匹配
                    match = re.match(self.printerData.single_logs[str(i)],log[2])
                    if match:
                        paper.normal_logs[str(i)] = log
                        self.dataProcessor.pap_logs.remove(log)
                        remove_flag = True
                        
                        # 从部分正常系log中提取参数信息(每个 case 分支都是独立的，执行完一个 case 分支后会自动跳出 match 语句，不会继续执行后续的 case 分支。)
                        match i:
                            case 1:
                                paper.page_num = match.group(1)
                            case 3:
                                paper.subscan = match.group(1)
                            case 4:
                                paper.trans = match.group(1)
                            case 10:
                                paper.tray1_space = match.group(1)
                            case 11:
                                paper.manual_space = match.group(1)
                            case 12:
                                paper.tray1_release_time = match.group(1)
                            case 13:
                                paper.manual_release_time = match.group(1)
                            case 20:
                                paper.actual_length = match.group(1)

                    # 异常系log匹配
                    else:
                        for j in range(1, abnm_num+1):
                            match = re.match(self.printerData.jam_logs[str(j)],log[2])
                            if match and match.group(1) == paper.id:
                                paper.abnormal_logs[str(j)] = log
                                self.dataProcessor.pap_logs.remove(log)
                                remove_flag = True
                                break
                    if remove_flag:
                        break
                        
            # 打印log信息
            # print("正常系log信息:", paper.normal_logs)
            # print("异常系log信息:", paper.abnormal_logs)
            # print("纸张信息1:", paper)

    def calculate_paper_info(self):
        """计算纸张信息"""
        # 需要计算的数据个数
        calculate_num = self.printerData.speed_info['key_node_number']
        for i in range(self.paper_count):
            paper = self.papers[i]
            # 速度判断
            if paper.speed == '0':
                standard = self.printerData.normal_speed
            elif paper.speed == '1':
                standard = self.printerData.middle_speed
            else:
                standard = self.printerData.slow_speed
            # 正常系log计算
            for j in range(1, calculate_num+1):
                # 获取计算log起始位置及标准时间
                start = standard[self.printerData.speed_info[str(j)]]['Start']
                end = standard[self.printerData.speed_info[str(j)]]['End']
                standard_time = standard[self.printerData.speed_info[str(j)]]['Value']
                # 计算时序及偏差
                if end in paper.normal_logs and start in paper.normal_logs:
                    if int(end) > int(start):
                        acl_time = int(paper.normal_logs[end][0]) - int(paper.normal_logs[start][0])
                        paper.trajectory_map[self.printerData.speed_info[str(j)]] = \
                            [standard_time, acl_time, standard_time - acl_time]
                    elif int(end) < int(start) and i < (self.paper_count-1) and end in self.papers[i+1].normal_logs:
                        acl_time = int(self.papers[i+1].normal_logs[end][0]) - int(paper.normal_logs[start][0])
                        paper.trajectory_map[self.printerData.speed_info[str(j)]] = \
                            [standard_time, acl_time, standard_time - acl_time]
                    else:
                        paper.trajectory_map[self.printerData.speed_info[str(j)]] = [standard_time, -1, -1]
            # print("纸张信息2:", paper)

    def print_papers(self):
        """输出所有纸张信息"""
        for paper in self.papers:
            print(paper)