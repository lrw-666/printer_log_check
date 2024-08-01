class Paper:
    def __init__(self, ID=None, speed=None, ftray=None, etray=None, length=None, width=None, thickness=None,
                 subscan=None, trans=None, tray1_space=None, manual_space=None, tray1_release_time=None, manual_release_time=None):
        self.ID = ID  # 纸张ID
        self.speed = speed  # 速度
        self.ftray = ftray  # 进纸口
        self.etray = etray  # 出纸口
        self.length = length  # 长
        self.width = width  # 宽
        self.thickness = thickness  # 厚度
        self.subscan = subscan  # 余白
        self.trans = trans  # 转印时间
        self.tray1_space = tray1_space  # 标准纸间距
        self.manual_space = manual_space  # 手送纸间距
        self.tray1_release_time = tray1_release_time  # 标准纸间释放时间
        self.manual_release_time = manual_release_time  # 手送纸间释放时间
        self.trajectory_map = {}  # 打印机中的运动轨迹，内容为路径名：时间
        self.normal_logs = []  # 正常系log名：时间
        self.abnormal_logs = []  # 异常系log：时间

    def __str__(self):
        return f"Paper(ID={self.ID}, speed={self.speed}, ftray={self.ftray}, etray={self.etray}, length={self.length},\
          width={self.width}, thickness={self.thickness}, subscan={self.subscan}, trans={self.trans},\
          tray1_space={self.tray1_space}, manual_space={self.manual_space}, tray1_release_time={self.tray1_release_time},\
          manual_release_time={self.manual_release_time}, trajectory_map={self.trajectory_map},\
          normal_logs={self.normal_logs}, abnormal_logs={self.abnormal_logs})"

    def add_trajectory(self, path_name, time):
        """添加新的运动轨迹"""
        self.trajectory_map[path_name] = time

    def get_trajectory(self, path_name):
        """获取运动轨迹"""
        return self.trajectory_map.get(path_name, None)

    def add_normal_log(self, log_name, time):
        """添加正常系log"""
        self.normal_logs.append((log_name, time))

    def add_abnormal_log(self, log_name, time):
        """添加异常系log"""
        self.abnormal_logs.append((log_name, time))

# 示例
if __name__ == "__main__":
    paper = Paper(ID="P123", speed="100mm/s", ftray="Tray1", etray="Tray2", length=297, width=210, thickness=0.1,
                  subscan=5, trans=15, tray1_space=560, manual_space=430, tray1_release_time=2372, manual_release_time=2594)
    print(paper)
    paper.add_trajectory("Path1", "10:00")
    paper.add_trajectory("Path2", "10:05")
    print(paper.get_trajectory("Path1"))
    paper.add_normal_log("Print Cnt[1], Sid[0]", "10:01")
    paper.add_abnormal_log("Jam Act Sid[2] Code[49]", "10:02")
    print(paper)
