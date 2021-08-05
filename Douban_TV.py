# -*- coding:utf-8 -*-

# 豆瓣 电视剧 全部类型 全部地区 全部年代 全部特色 前200名
# 豆瓣 电视剧 全部类型 全部地区 2021 全部特色 前200名
# 豆瓣 电视剧 全部类型 全部地区 2020 全部特色 前200名
# 豆瓣 电视剧 全部类型 全部地区 2019 全部特色 前200名

import requests
from bs4 import BeautifulSoup
import xlwt
import os
import time
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_url(year, page):
    if year == 'all_age':
        url_g = 'https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=%E7%94%B5%E8%A7%86%E5%89%A7&start=' \
              + str(20 * (page - 1))
    else:
        url_g = 'https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=%E7%94%B5%E8%A7%86%E5%89%A7&start=' \
              + str(20 * (page - 1)) + '&year_range=' + year + ',' + year
    return url_g


if __name__ == '__main__':
    if os.path.exists('Douban_TV.csv'):
        os.remove('Douban_TV.csv')
    year_crawler = ['all_age', '2021', '2020', '2019']
    work_book = xlwt.Workbook()
    for item_age in year_crawler:
        work_sheet = work_book.add_sheet('Douban_TV_' + item_age)
        work_sheet.write(0, 0, 'title')
        work_sheet.write(0, 1, 'Url')
        work_sheet.write(0, 2, 'casts')
        work_sheet.write(0, 3, 'Star Rate')
        work_sheet.write(0, 4, 'Rating')
        work_sheet.write(0, 5, 'directors')
        work_sheet.write(0, 6, 'cover')
        column = 1
        for i in range(1, 21, 1):
            url = get_url(item_age, i)
            print(url)
            my_header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                        "Chrome/92.0.4515.107 Safari/537.36 "
            headers = {
                'Host': 'movie.douban.com',  # 请求来源
                'Referer': 'https://movie.douban.com/tag/',  # 请求来源，携带的信息比“origin”更丰富，
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55',
            }

            response = requests.get(url, headers=headers, timeout=10)
            json_comment = response.json()
            for try_times in range(3):
                print('try_times : %i' % try_times)
                if 'data' in json_comment.keys():
                    break
                else:
                    print(json_comment['msg'])
                    for wait_time in range(60):
                        print('wait time %is ...' % wait_time)
                        time.sleep(1)
                    response = requests.get(url, headers=headers, timeout=10)
                    json_comment = response.json()

            list_comment = json_comment['data']
            for item in list_comment:
                cast_string = ''
                director_string = ''
                print(str(i) + '  ' + str(item['title']) + '  ' + str(item['url']) + '  ' + str(item['casts']) + '  ' +
                    str(item['star']) + '  ' + str(item['rate']) + '  ' + str(item['directors']) + '  '
                    + str(item['cover']))
                for item_casts in item['casts']:
                    cast_string = cast_string + str(item_casts) + ' '
                for item_director in item['directors']:
                    director_string = director_string + str(item_director) + ' '

                work_sheet.write(column, 0, item['title'])
                work_sheet.write(column, 1, item['url'])
                work_sheet.write(column, 2, cast_string.decode('utf-8'))
                work_sheet.write(column, 3, str(int(item['star']) / 10.0))
                work_sheet.write(column, 4, item['rate'])
                work_sheet.write(column, 5, director_string.decode('utf-8'))
                work_sheet.write(column, 6, item['cover'])
                column = column + 1

    work_book.save('Douban_TV.csv')
