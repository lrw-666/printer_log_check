class Paper:
    def __init__(self, id=None, speed=None, ftray=None, etray=None, length=None, width=None, thickness=None):
        self.id = id  # 纸张ID
        self.speed = speed  # 速度
        self.ftray = ftray  # 进纸口
        self.etray = etray  # 出纸口
        self.length = length  # 长
        self.width = width  # 宽
        self.thickness = thickness  # 厚度
        self.page_num = -1  # 页数
        self.subscan = -1  # 余白
        self.trans = -1  # 转印时间
        self.tray1_space = -1  # 标准纸间距
        self.manual_space = -1  # 手送纸间距
        self.tray1_release_time = -1  # 标准纸间释放时间
        self.manual_release_time = -1  # 手送纸间释放时间
        self.actual_length = -1  # 实际检测纸长
        self.trajectory_map = {}  # 打印机中的运动轨迹，内容为路径名：时间
        self.normal_logs = {}  # 正常系log名：时间
        self.abnormal_logs = {}  # 异常系log：时间

    def __str__(self):
        return f"Paper(id={self.id}, speed={self.speed}, ftray={self.ftray}, etray={self.etray}, length={self.length},\
          width={self.width}, thickness={self.thickness}, subscan={self.subscan}, trans={self.trans}, page={self.page_num},\
          tray1_space={self.tray1_space}, manual_space={self.manual_space}, tray1_release_time={self.tray1_release_time},\
          manual_release_time={self.manual_release_time}, actual_length={self.actual_length}, trajectory_map={self.trajectory_map},\
          normal_logs={self.normal_logs}, abnormal_logs={self.abnormal_logs})"

# 示例
if __name__ == "__main__":
    paper = Paper(id="P123", speed="100mm/s", ftray="Tray1", etray="Tray2", length=297, width=210, thickness=0.1,
                  subscan=5, trans=15, tray1_space=560, manual_space=430, tray1_release_time=2372, manual_release_time=2594)
    print(paper)
