from data_processor import DataProcessor
from excel_com import ExcelHandler
from paper_ctrl import PaperController
from paper import Paper
from printer_data import PrinterData

"""全局变量"""
json_path = "printer_config.json"

# 主函数
def main():
    print("This is the main function of printer_main.py")
    # 获取配置文件json对象
    printer_data = PrinterData(json_path)
    # 读取n行log文件，并进行初步处理——筛选出打印管理的纸sheet数据与纸搬送log
    data_processor = DataProcessor(printer_data.file_path, printer_data, 1000)
    # 建立纸管理对象，并将纸数据导入，动态生成纸对象
    paper_controller = PaperController(printer_data, data_processor)
    paper_controller.add_paper()
    # 动态分配纸搬送信息
    paper_controller.allocate_PAP_info()
    # 计算纸搬送时序
    paper_controller.calculate_paper_info()
    # 获取Excel文件路径，并创建ExcelHandler对象
    excel_handler = ExcelHandler(printer_data.excel_path, data_processor, paper_controller)
    # 保存任务信息到task_massage页面
    excel_handler.save_task_massage()
    # 保存纸搬送Log到paper_Log页面
    excel_handler.save_pap_logs()
    # 保存各页面信息到paper_n文件
    excel_handler.save_paper_n()
    # 关闭Excel文件
    excel_handler.close()

if __name__ == '__main__':
    main()