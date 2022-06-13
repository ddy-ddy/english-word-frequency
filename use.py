# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 11:31 AM
# @Author  : ddy
# @FileName: use.py
# @github  : https://github.com/ddy-ddy

import json
import os


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
    data = get_data_from_json(f"examination_use_words_data/2006.json")
    data = data["text_1"]

    for item in data:
        # headWord
        print(f"#### {item['headWord']}")

        # headWord trans
        for _ in item["headTrans"]:
            print(f"`{_['pos']}`. {_['trans']}")
            print("\n")

        # example
        for i, _ in enumerate(item["example"]):
            print(f"- {_['sentence']}")
            print(f" {_['trans']}")

        # phrase

        print("------")
