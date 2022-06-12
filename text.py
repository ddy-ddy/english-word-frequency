# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 12:56 AM
# @Author  : ddy
# @FileName: text.py
# @github  : https://github.com/ddy-ddy
import json


def get_data_from_json(json_path):
    '''
    从json数据中得到info标签的数据
    :param json_path:json文件
    :return: json数据
    '''
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data


if __name__ == '__main__':
    data = get_data_from_json("examination_use_words_data/2006.json")
    print(data)
