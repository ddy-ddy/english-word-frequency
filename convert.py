# -*- coding: utf-8 -*-
# @Time    : 2022/6/12 11:00 PM
# @Author  : ddy
# @FileName: convert.py
# @github  : https://github.com/ddy-ddy

'''
将原始的original单词数据转换为自己使用的json数据
原始文件：original.json
转换后的文件：kaoyan_data.json
格式为：
    {
        "headWord": "about",
        "headTrans": [{"pos":'v',"trans":"关于"},{},{}],
        "example":[{"sentence":"this is about how to do","trnas":"这是关于"},{},{}],
        "phrase":[{"name":"about to","trnas":"关于"},{}],
        "realWord":[{"name":"abouts","pos":"v","trans":"关于ing"},{},{}]
        "allWord":[],
    }
'''
import json


def dump_dict_to_json_file(json_path, dict_info):
    '''
    将dict的数据导入到json文件中
    :param json_path: json文件路径
    :param dict_info: dict数据
    '''
    json_info = json.dumps(dict_info, ensure_ascii=False, indent=4)
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(json_info)


def get_kaoyan_data():
    # 读取原json中的数据,并重构json格式
    info = []
    words = []
    with open("vocabulary_data/original.json", 'r') as f:
        for line in f.readlines():
            temp_info = eval(line)
            temp_add_info = {"headWord": "", "headTrans": [], "example": [], "phrase": [], "realWord": []}
            # headWord
            temp_add_info["headWord"] = temp_info["content"]["word"]["wordHead"]

            # headTrans
            if "trans" in list(temp_info["content"]["word"]["content"].keys()):
                temp_add_headTrans = []
                for item in temp_info["content"]["word"]["content"]["trans"]:
                    temp_add_headTrans.append({"pos": item["pos"], "trans": item["tranCn"]})
                temp_add_info["headTrans"] = temp_add_headTrans

            # example
            if "sentence" in list(temp_info["content"]["word"]["content"].keys()):
                temp_add_example = []
                for item in temp_info["content"]["word"]["content"]["sentence"]["sentences"]:
                    temp_add_example.append({"sentence": item["sContent"], "trnas": item["sCn"]})
                temp_add_info["example"] = temp_add_example

            # phrase
            if "phrase" in list(temp_info["content"]["word"]["content"].keys()):
                temp_add_phrase = []
                for item in temp_info["content"]["word"]["content"]["phrase"]["phrases"]:
                    temp_add_phrase.append({"name": item["pContent"], "trnas": item["pCn"]})
                temp_add_info["phrase"] = temp_add_phrase

            # realWord and allWord
            if "relWord" in list(temp_info["content"]["word"]["content"].keys()):
                temp_add_realWord = []
                temp_all_word = [temp_info["content"]["word"]["wordHead"]]
                for item in temp_info["content"]["word"]["content"]["relWord"]["rels"]:
                    if "pos" in list(item.keys()):
                        pos = item["pos"]
                        for _ in item["words"]:
                            temp_add_realWord.append({"name": _["hwd"], "pos": pos, "trans": _["tran"]})
                            temp_all_word.append(_["hwd"])
                words.append(temp_all_word)
                temp_add_info["allWord"] = temp_all_word
                temp_add_info["relWord"] = temp_add_realWord
            info.append(temp_add_info)
    f.close()
    dump_dict_to_json_file("vocabulary_data/kaoyan_data.json", info)
    return info, words


if __name__ == '__main__':
    get_kaoyan_data()
