import json

class PrinterData:
    def __init__(self, json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            print("JSON Data:", data)  # 调试信息：打印解析后的JSON数据
            
            self.printer_name = data.get('printer_name', 'Unknown')
            self.version = data.get('version', 'Unknown')
            self.paper_info = data.get('paper_info', {})
            self.single_logs = data.get('single_logs', {})
            self.jam_logs = data.get('jam_logs', {})
            self.speed_info = data.get('speed_info', {})
            self.normal_speed = data.get('nomral_speed', {})
            self.middle_speed = data.get('middle_speed', {})
            self.slow_speed = data.get('slow_speed', {})
        except FileNotFoundError:
            print(f"Error: File {json_file} not found.")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in file {json_file}.")
        except KeyError as e:
            print(f"Error: Key {e} not found in JSON file.")

    def display_info(self):
        print(f"Printer Name: {self.printer_name}")
        print(f"Version: {self.version}")

    def display_paper_info(self):
        print("\nPaper Info:")
        for key, value in self.paper_info.items():
            print(f"{key}: {value}")

    def display_single_logs(self):
        print("\nSingle Logs:")
        for key, value in self.single_logs.items():
            print(f"{key}: {value}")

    def display_jam_logs(self):
        print("\nJam Logs:")
        for key, value in self.jam_logs.items():
            print(f"{key}: {value}")

    def display_speeds(self):
        print("\nSpeed Info:")
        for key, value in self.speed_info.items():
            print(f"{key}: {value}")

        print("\nNormal Speed:")
        for key, value in self.normal_speed.items():
            print(f"{key}: {value}")

        print("\nMiddle Speed:")
        for key, value in self.middle_speed.items():
            print(f"{key}: {value}")

        print("\nSlow Speed:")
        for key, value in self.slow_speed.items():
            print(f"{key}: {value}")

# 示例使用
if __name__ == "__main__":
    printer_data = PrinterData('printer_config.json')
    printer_data.display_info()
    printer_data.display_paper_info()
    printer_data.display_single_logs()
    printer_data.display_jam_logs()
    printer_data.display_speeds()
