import csv
import json
import yaml
import os

def load_csv_data(file_path):
    """从 CSV 文件读取测试数据，返回列表，每条数据为一个元组"""
    data = []
    base_dir = os.path.dirname(os.path.dirname(__file__))
    full_path = os.path.join(base_dir, file_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 将行转换为元组，顺序与表头一致
            # 注意 CSV 第一行是: username,password,expected_result
            data.append((row['username'], row['password'], row['expected_result']))
    return data

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_yaml_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)