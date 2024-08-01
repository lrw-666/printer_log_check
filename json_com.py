import json

class JsonConverter:

    @staticmethod
    def to_json(data_map):
        # 将Python的dict对象转换为JSON字符串
        if not isinstance(data_map, dict):
            raise ValueError("Input should be a dictionary")
        return json.dumps(data_map, ensure_ascii=False, indent=4)

    @staticmethod
    def from_json(json_str):
        # 将JSON字符串转换为Python的dict对象
        return json.loads(json_str)
    
    @staticmethod
    def save_to_file(data_map, file_path):
        # 将Python的dict对象保存到JSON文件中
        if not isinstance(data_map, dict):
            raise ValueError("Input should be a dictionary")
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data_map, file, ensure_ascii=False, indent=4) # 

    @staticmethod
    def load_from_file(file_path):
        # 从JSON文件中读取Python的dict对象
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

# 示例用法
if __name__ == "__main__":
    config = {
        "app_name": "MyApp",
        "version": "1.0",
        "settings": {
            "debug": True,
            "log_level": "INFO"
        }
    }

    # json_str = JsonConverter.to_json(config)
    # print("JSON String:")
    # print(json_str)

    # restored_config = JsonConverter.from_json(json_str)
    # print("\nRestored Config:")
    # print(restored_config)

    # 将dict保存到JSON文件
    JsonConverter.save_to_file(config, 'printer_config.json')

    # 从JSON文件读取并转换为dict
    restored_config = JsonConverter.load_from_file('printer_config.json')
    print("Restored Config:")
    print(restored_config)
