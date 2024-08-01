from paper import Paper  # 导入Paper类

class PaperController:
    def __init__(self):
        self.papers = []  # 存储所有纸张对象
        self.paper_count = 0  # 纸张数量
        self.paper_spacing = 0  # 前后纸间距
        self.path_map = {}  # 参考路径map，记录路径出现次数

    def add_paper(self, paper):
        """添加纸张对象"""
        self.papers.append(paper)
        self.paper_count += 1

    def generate_paper(self, log_line):
        """根据log生成纸张对象"""
        # 假设log_line中包含纸张的属性信息
        # 这里可以根据实际log格式解析出纸张的属性
        attributes = self.parse_log(log_line)
        if attributes:
            paper = Paper(**attributes)
            self.add_paper(paper)
            return paper
        return None

    def parse_log(self, log_line):
        """解析log, 返回纸张属性字典"""
        # 这里假设log_line的格式为 "ID=P123,speed=100mm/s,ftray=Tray1,etray=Tray2,length=297,width=210,thickness=0.1"
        attributes = {}
        for item in log_line.split(','):
            key, value = item.split('=')
            attributes[key] = value
        return attributes

    def match_path(self, path_name):
        """路径匹配，记录路径出现次数"""
        if path_name in self.path_map:
            self.path_map[path_name] += 1
        else:
            self.path_map[path_name] = 1

    def print_papers(self):
        """输出所有纸张信息"""
        for paper in self.papers:
            print(paper)

# 示例
if __name__ == "__main__":
    controller = PaperController()

    # 模拟log文件
    log_lines = [
        "ID=P123,speed=100mm/s,ftray=Tray1,etray=Tray2,length=297,width=210,thickness=0.1",
        "ID=P456,speed=150mm/s,ftray=Tray2,etray=Tray3,length=210,width=148,thickness=0.08"
    ]

    # 根据log生成纸张对象
    for log_line in log_lines:
        controller.generate_paper(log_line)

    # 路径匹配
    controller.match_path("Path1")
    controller.match_path("Path2")
    controller.match_path("Path1")

    # 输出所有纸张信息
    controller.print_papers()

    # 输出路径匹配结果
    print(controller.path_map)
