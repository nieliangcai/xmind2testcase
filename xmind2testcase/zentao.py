#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import csv
import logging
import os
import re

from const import CASE_MODULE
from utils import get_xmind_testcase_list, get_absolute_path

"""
Convert XMind fie to Zentao testcase csv file 

Zentao official document about import CSV testcase file: https://www.zentao.net/book/zentaopmshelp/243.mhtml 
"""

def xmind_to_zentao_csv_file(xmind_file):
    """Convert XMind file to a zentao csv file"""
    xmind_file = get_absolute_path(xmind_file)
    logging.info('Start converting XMind file(%s) to zentao file...', xmind_file)
    testcases = get_xmind_testcase_list(xmind_file)

    fileheader = ["所属模块", "用例标题", "前置条件", "步骤", "预期", "关键词", "优先级", "用例类型", "适用阶段"]  # , "相关需求"]
    zentao_testcase_rows = [fileheader]
    for testcase in testcases:
        row = gen_a_testcase_row(testcase)
        zentao_testcase_rows.append(row)

    zentao_file = xmind_file[:-6] + '.csv'
    if os.path.exists(zentao_file):
        os.remove(zentao_file)
        # logging.info('The zentao csv file already exists, return it directly: %s', zentao_file)
        # return zentao_file

    with open(zentao_file, 'w', encoding='utf8', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(zentao_testcase_rows)
        logging.info('Convert XMind file(%s) to a zentao csv file(%s) successfully!', xmind_file, zentao_file)

    return zentao_file


def gen_a_testcase_row(testcase_dict):
    case_module = "/导入测试用例(#2862)"  # gen_case_module(testcase_dict['suite'])
    case_title = gen_case_module(testcase_dict['suite']) + " " + testcase_dict['name']
    print(11111111111, case_title)

    string = ""
    if "&" in case_title:
        # a = case_title.split("&")[:-1]
        string_prefix = case_title.split("&")[:-1]
        string_suffix = case_title.split("&")[-1]
        print(string_prefix, string_suffix)
        for i in string_prefix:
            b = i.strip().split(" ")[:-1]
            for j in b:
                if j:
                    string += f"【{j}】"
        for i in [string_suffix]:
            b = i.strip().split(" ")[:-1]
            for j in b:
                if j:
                    string += f"【{j}】"
        string += str(string_suffix.split(" ")[-1]).strip()
    else:
        a = case_title.strip().split(" ")[:-1]
        for j in a:
            if j:
                string += f"【{j}】"
        string += str(case_title.split(" ")[-1]).strip()
        print(string)

    case_title = string
    print(f"修改后的case标题为:{case_title}")

    case_precontion = testcase_dict['preconditions']
    case_step, case_expected_result = gen_case_step_and_expected_result(testcase_dict['steps'])
    case_keyword = ''
    case_priority = gen_case_priority(testcase_dict['importance'])
    from pprint import pprint
    pprint(testcase_dict)
    case_type = gen_case_type(testcase_dict['execution_type'])
    case_apply_phase = gen_case_apply_phase("dev") if str(testcase_dict['name']).__contains__(
        "dev") else gen_case_apply_phase(
        testcase_dict['importance'])
    case_prd = testcase_dict['summary']
    row = [case_module, case_title, case_precontion, case_step, case_expected_result, case_keyword, case_priority,
           case_type, case_apply_phase]  # , case_prd]
    return row


def gen_case_module(module_name):
    if module_name:
        module_name = module_name.replace('（', '(')
        module_name = module_name.replace('）', ')')
    else:
        module_name = '/'
    return module_name


def gen_case_step_and_expected_result(steps):
    case_step = ''
    case_expected_result = ''

    for step_dict in steps:
        case_step += str(step_dict['step_number']) + '. ' + step_dict['actions'].replace('\n', '').strip() + '\n'
        case_expected_result += str(step_dict['step_number']) + '. ' + \
                                step_dict['expectedresults'].replace('\n', '').strip() + '\n' \
            if step_dict.get('expectedresults', '') else ''

    return case_step, case_expected_result


def gen_case_priority(priority):
    mapping = {1: 1, 2: 2, 3: 3, 4: 4}
    if priority in mapping.keys():
        return mapping[priority]
    else:
        return 2


def gen_case_apply_phase(priority):
    mapping = {1: "冒烟测试阶段", 2: "功能测试阶段", 3: "功能测试阶段", 4: "功能测试阶段", "dev": "冒烟测试阶段"}
    if priority in mapping.keys():
        return mapping[priority]
    else:
        return 2


def gen_case_type(case_type):
    mapping = {1: '功能测试', 2: '自动化测试', 3: "接口测试"}
    if case_type in mapping.keys():
        return mapping[case_type]
    else:
        return "功能测试"
        # return f'{case_type}'



if __name__ == '__main__':
    xmind_file_path = fr'D:\01 业务文件\01 测试用例\420统计中心.xmind'
    zentao_csv_file = xmind_to_zentao_csv_file(xmind_file_path)
    print(f'已成功将xmind用例转换为禅道csv文件: {zentao_csv_file}')
