# -*- coding: utf-8 -*-
# @Time    : 2022/6/12 11:08 AM
# @Author  : ddy
# @FileName: main.py
# @github  : https://github.com/ddy-ddy

'''
1. 读取txt里面的文件作为一个字符串
2. 对字符串进行预处理
    - 删除特殊符号
    - 删除数字
    - 删除停用词
'''

from string import punctuation
import re
import spacy
import json

nlp = spacy.load("en_core_web_lg")


def dump_dict_to_json_file(json_path, dict_info):
    '''
    将dict的数据导入到json文件中
    :param json_path: json文件路径
    :param dict_info: dict数据
    '''
    json_info = json.dumps(dict_info, ensure_ascii=False, indent=4)
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(json_info)


def preprocess_content(content):
    '''
    对文章进行预处理
    :param content:
    :return:
    '''
    preprocessed_data, no_use_token = [], ["\n", "’s", "’t", "“", "” ", " ” ", " ”", "’", " ’", " ’ ", "’ "]
    # 去除标点符号
    for char in content:
        char = re.sub(r'[{}]+'.format(punctuation), ' ', char)
        char = char.lower()
        preprocessed_data.append(char)
    preprocessed_data = "".join(preprocessed_data)
    # 去除自定义不使用的符号
    for token in no_use_token:
        preprocessed_data = preprocessed_data.replace(token, " ")
    # 去除长度小于等于2的单词
    preprocessed_data = " ".join([word for word in preprocessed_data.split() if len(word) > 2])

    # 使用spacy去除停用词，得到有用的单词
    useful_word = []
    for token in nlp(preprocessed_data):
        if not token.is_stop:
            useful_word.append(token.lemma_.lower())
    useful_word = list(set(useful_word))  # 去重
    return useful_word


def get_data_from_json(json_path):
    '''
    从json数据中得到info标签的数据
    :param json_path:json文件
    :return: json数据
    '''
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data


def get_kaoyan_data():
    # 读取json中的数据
    info = get_data_from_json("vocabulary_data/kaoyan_data.json")
    words = []
    for item in info:
        if "allWord" in list(item.keys()):
            words.append(item["allWord"])
        else:
            words.append([])
    return info, words


def get_split_context(file_path):
    # 得到某张试卷的所有内容
    with open(file_path, 'r', encoding="utf-8") as f:
        content = f.read()
        content = content.replace("\n", " ")  # 去除转行符
    f.close()

    # 拆分试卷
    content_split_result = {
        "text_1": re.findall(r'Section I Use of English(.*?)Section II Reading Comprehension', content)[0],  # 完型填空
        "reading_1": re.findall(r'Text 1(.*?)Text 2', content)[0],  # 第一篇阅读
        "reading_2": re.findall(r'Text 2(.*?)Text 3', content)[0],  # 第二篇阅读
        "reading_3": re.findall(r'Text 3(.*?)Text 4', content)[0],  # 第三篇阅
        "reading_4": re.findall(r'Text 4(.*?)Part B', content)[0],  # 第四篇阅读
        "other_text": re.findall(r'Part B(.*?)20 points', content)[0]  # 其他内容
    }
    return content_split_result


if __name__ == '__main__':
    # 得到考研所有的单词数据
    kaoyan_info, kaoyan_words = get_kaoyan_data()
    assert len(kaoyan_info) == len(kaoyan_words)

    # 得到试卷的不同内容
    split_content = get_split_context("examination_data/2006.txt")

    for key in split_content:
        useful_word = preprocess_content(split_content[key])  # 得到试卷上有用的单词
        contained_words_info = []  # 包含的单词的信息
        # 遍历有用的单词
        for word in useful_word:
            # 遍历所有的考研单词，看看有用的单词是否在里面，如果在里面则保存信息
            for j, temp in enumerate(kaoyan_words):
                if word in temp and kaoyan_info[j] not in contained_words_info:  # 保证去重
                    contained_words_info.append(kaoyan_info[j])
        split_content[key] = contained_words_info

    dump_dict_to_json_file("examination_use_words_data/2006.json", split_content)  # 保存数据



