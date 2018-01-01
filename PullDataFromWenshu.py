# -*- coding: UTF-8 -*-

import csv
import argparse
import os
import sys
import time
import json
import Spider
import CourtList
import FileUtils
import re

def refresh_total_number(search_criteria, case_folder):
    wenshu.set_search_criteria(search_criteria)
    total_number = wenshu.get_total_item_number()
    if total_number:
        try:
            f = open(case_folder + '\\total_number_' + str(total_number), 'x')
            f.close()
        except Exception as e:
            print(e)
        
        
def download_caselist(wenshu, search_criteria, case_folder):
    file_list = os.listdir(case_folder)

    if not file_list:
        csv_file = case_folder + '\\' + 'case_list_1.csv'
        total_number = wenshu.get_case_list(1)
        FileUtils.dump2csv(wenshu.case_brief, csv_file)
        f = open(case_folder + '\\total_number_' + str(total_number), 'x')
        f.close()
        max_page = int(total_number) // 20
        if int(total_number) % 20:
            max_page += 1
        for index in range(2, max_page + 1):
            csv_file = case_folder + '\\' + 'case_list_' + str(index) + '.csv'
            wenshu.get_case_list(index)
            FileUtils.dump2csv(wenshu.case_brief, csv_file)
            time.sleep(10)
    else:
        for file in file_list:
            if 'total_number' in file:
                total_number = file[13:]
                max_page = int(total_number) // 20
                if int(total_number) % 20:
                    max_page += 1
        #case_list_number = len(file_list)
        #print(case_list_number - 1)
        for index in range(1, max_page + 1):
            csv_file = case_folder + '\\' + 'case_list_' + str(index) + '.csv'
            if not os.path.exists(csv_file) or os.path.getsize(csv_file) < 1000:
                wenshu.get_case_list(index)
                FileUtils.dump2csv(wenshu.case_brief, csv_file)
                print('Sleep 10s.....')
                time.sleep(10)

def debug_download_single_list(wenshu, search_criteria, case_folder, index):
    csv_file = case_folder + '\\' + 'case_list_' + index + '.csv'
    wenshu.set_search_criteria(search_criteria)
    wenshu.get_case_list(index)
    FileUtils.dump2csv(wenshu.case_brief, csv_file)


def download_case(wenshu, case_id):
    return wenshu.get_case(case_id)


def debug_download_case(wenshu, doc_id):
    t = download_case(wenshu, doc_id)
    print(t)



def main():
    year = '2014'
    #court = '自贡市自流井区人民法院'
    #court = '黑水县人民法院'
    #court = '二审'
    base_dir = 'C:\\Users\\lij37\\Cases'
    #case_list_dir = base_dir + '\\' + year + '\\' + court
    case_dir = base_dir + '\\' + year + '\\' + '案件'
    debug_case_id = '2db9117a-d235-4f8d-8bd7-57f7029f2546'
    #path = 'C:\\Users\\lij37\\Code\\NewHan' + year + '\\'
    #court = '自贡市自流井区人民法院'
    #court = '黑水县人民法院'
    #search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:" + year +",文书类型:判决书," + "基层法院:" + court
    #search_criteria = "案件类型:刑事案件,审判程序:二审,法院地域:四川省,裁判年份:" + year + ",文书类型:判决书"
    court_list = ['成都市锦江区人民法院', '成都市青羊区人民法院', '成都市金牛区人民法院',
                    '成都市武侯区人民法院', '成都市成华区人民法院', '成都市龙泉驿区人民法院', '成都市青白江区人民法院',
                    '成都市温江区人民法院', '金堂县人民法院', '双流区人民法院', '郫县人民法院',
                    '大邑县人民法院', '蒲江县人民法院', '新津县人民法院', '都江堰市人民法院', '彭州市人民法院',
                    '邛崃市人民法院', '崇州市人民法院', '成都高新技术产业开发区人民法院']

    # wenshu = Spider.WenShu()
    # debug_download_case(wenshu, debug_case_id)
    # court = '自贡市大安区人民法院'
    # search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:" + year + ",文书类型:判决书," + "基层法院:" + court
    # case_list_dir = base_dir + '\\' + year + '\\' + court
    # debug_download_single_list(wenshu, search_criteria, case_list_dir, '1')
    # return None

    for court in court_list:
        wenshu = Spider.WenShu()
        search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:" + year + ",文书类型:判决书," + "基层法院:" + court
        wenshu.set_search_criteria(search_criteria)
        case_list_dir = base_dir + '\\' + year + '\\' + court
        FileUtils.validate_path(case_list_dir)
        download_caselist(wenshu, search_criteria, case_list_dir)
    return None

    #refresh_total_number(wenshu, search_criteria, case_list_dir)
    #case_list = FileUtils.read_csv('C:\\Users\\lij37\\Code\\NewHan2017\\自贡市自流井区人民法院\\case_list_1.csv')
    #case_name = '周某某危险驾驶一案一审判决书'
    #case_id = 'a9a069cd-832a-4f22-a576-a74d0123ca00'
    FileUtils.validate_path(case_dir)
    file_list = os.listdir(case_list_dir)
    for file in file_list:
        if 'csv' in file:
            case_list = FileUtils.read_csv(case_list_dir + '\\' + file)
            for i in range(len(case_list['name'])):
                #if case_list['download'][i] != 'Y':
                case_file = case_dir + '\\' + case_list['name'][i] + '_' + case_list['doc_id'][i] + '.txt'
                if not os.path.exists(case_file) or os.path.getsize(case_file) < 1000:
                    print("Case {} in {}: {} {} is downloading...".format(i, file, case_list['name'][i], case_list['doc_id'][i]))
                    t = download_case(wenshu, case_list['doc_id'][i])
                    if t:
                        try:
                            FileUtils.write_text(case_file, t)
                            case_list['download'][i] = 'Y'
                            time.sleep(3)
                        except Exception as e:
                            print(e)
                            case_list['download'][i] = 'Invalid'
                    else:
                        case_list['download'][i] = 'Invalid'
            FileUtils.dump2csv(case_list, case_list_dir + '\\' + file)

if __name__ == "__main__":
    main()

