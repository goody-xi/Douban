# -*- coding:utf-8 -*-

# 爬取豆瓣关于剧情的影视 前15页

import requests
import urllib2
from bs4 import BeautifulSoup
import xlwt
import os
import time

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_url(Movie_type, page):
    if Movie_type == 'JuQing':
        if page == 1:
            url = 'https://www.douban.com/tag/%E5%89%A7%E6%83%85/movie'
        else:
            temp_string = '?start=' + str((page - 1) * 15)
            url = 'https://www.douban.com/tag/%E5%89%A7%E6%83%85/movie' + temp_string
    elif Movie_type == 'DongHua':
        if page == 1:
            url = 'https://www.douban.com/tag/%E5%8A%A8%E7%94%BB/movie'
        else:
            temp_string = '?start=' + str((page - 1) * 15)
            url = 'https://www.douban.com/tag/%E5%8A%A8%E7%94%BB/movie' + temp_string
    elif Movie_type == 'FanZui':
        if page == 1:
            url = 'https://www.douban.com/tag/%E7%8A%AF%E7%BD%AA/movie'
        else:
            temp_string = '?start=' + str((page - 1) * 15)
            url = 'https://www.douban.com/tag/%E7%8A%AF%E7%BD%AA/movie' + temp_string
    elif Movie_type == 'JingSong':
        if page == 1:
            url = 'https://www.douban.com/tag/%E6%83%8A%E6%82%9A/movie'
        else:
            temp_string = '?start=' + str((page - 1) * 15)
            url = 'https://www.douban.com/tag/%E6%83%8A%E6%82%9A/movie' + temp_string
    elif Movie_type == 'XuanYi':
        if page == 1:
            url = 'https://www.douban.com/tag/%E6%82%AC%E7%96%91/movie'
        else:
            temp_string = '?start=' + str((page - 1) * 15)
            url = 'https://www.douban.com/tag/%E6%82%AC%E7%96%91/movie' + temp_string
    elif Movie_type == 'Cult':
        if page == 1:
            url = 'http://www.douban.com/tag/cult/movie'
        else:
            temp_string = '?start=' + str((page - 1) * 15)
            url = 'http://www.douban.com/tag/cult/movie' + temp_string
    elif Movie_type == 'KongBu':
        if page == 1:
            url = 'http://www.douban.com/tag/%E6%81%90%E6%80%96/movie'
        else:
            temp_string = '?start=' + str((page - 1) * 15)
            url = 'http://www.douban.com/tag/%E6%81%90%E6%80%96/movie' + temp_string
    elif Movie_type == 'BaoLi':
        if page == 1:
            url = 'http://www.douban.com/tag/%E6%9A%B4%E5%8A%9B/movie'
        else:
            temp_string = '?start=' + str((page - 1) * 15)
            url = 'http://www.douban.com/tag/%E6%9A%B4%E5%8A%9B/movie' + temp_string
    elif Movie_type == 'HeiBang':
        if page == 1:
            url = 'http://www.douban.com/tag/%E9%BB%91%E5%B8%AE/movie'
        else:
            temp_string = '?start=' + str((page - 1) * 15)
            url = 'http://www.douban.com/tag/%E9%BB%91%E5%B8%AE/movie' + temp_string
    else:
        url = 'https://www.douban.com/tag/%E5%89%A7%E6%83%85/movie'
    return url


def bs4_analyze(html_string):
    if BeautifulSoup(html_string, 'lxml').find('div', attrs={'class': 'mod movie-list'}) is None:
        return 'Error'
    else:
        table = BeautifulSoup(html_string, 'lxml').find('div', attrs={'class': 'mod movie-list'}).find_all('dl')

        movie_name = []
        movie_url = []
        movie_desc = []
        movie_star = []
        movie_rating = []

        name_temp_string = ''
        url_temp_string = ''
        desc_temp_string = ''
        star_temp_string = ''
        rating_temp_string = ''

        for item in table:
            name_temp_string = item.dd.a.string
            movie_name.append(name_temp_string)

            url_temp_string = item.find('a').get('href')
            movie_url.append(url_temp_string)

            desc_temp_string = item.dd.div.string
            movie_desc.append(desc_temp_string)

            print(item.span)
            if item.span is None:
                star_temp_string = 'NA'
                rating_temp_string = 'NA'
            else:
                star_temp_string = item.span['class'][0]
                star_temp_string = star_temp_string.replace('allstar', '')
                star_temp_string = str(int(star_temp_string) / 10.0)
                rating_temp_string = item.find(attrs={"class": 'rating_nums'}).string
            movie_star.append(star_temp_string)
            movie_rating.append(rating_temp_string)

            print(name_temp_string + '  ' + url_temp_string + '  ' + desc_temp_string[8:-7] + '  ' + star_temp_string +
              '  ' + rating_temp_string)

        return movie_name, movie_url, movie_desc, movie_star, movie_rating


if __name__ == '__main__':
    List_Movie_Type = ['JuQing', 'DongHua', 'FanZui', 'JingSong', 'XuanYi', 'Cult', 'KongBu', 'BaoLi', 'HeiBang']
    if os.path.exists('Douban_Movie.csv'):
        os.remove('Douban_Movie.csv')
    # List_Movie_Type = ['HeiBang']
    work_book = xlwt.Workbook()
    for item_movie_type in List_Movie_Type:
        column = 1
        work_sheet = work_book.add_sheet(item_movie_type, cell_overwrite_ok=True)
        work_sheet.write(0, 0, 'Name')
        work_sheet.write(0, 1, 'Url')
        work_sheet.write(0, 2, 'Type')
        work_sheet.write(0, 3, 'Star Rate')
        work_sheet.write(0, 4, 'Rating')
        for item_page in range(1, 16, 1):
            url = get_url(Movie_type=item_movie_type, page=item_page)
            my_header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                        "Chrome/92.0.4515.107 Safari/537.36 "
            req = urllib2.Request(url)
            req.add_header("User-Agent", my_header)

            MaximumTryTimes = 3
            for i in range(3):
                try:
                    response = urllib2.urlopen(req, timeout=5)
                    if response.getcode() == 200:
                        break
                except:
                    print('request %i times failed!!' % i)

            wbdata = response.read()
            #print('item page : %i   status code %s ' % (item_page, status_code))
            data = bs4_analyze(wbdata)
            if data == 'Error':
                continue
            else:
                for item in range(1, len(data[0]), 1):
                    work_sheet.write(column, 0, data[0][item - 1])
                    work_sheet.write(column, 1, data[1][item - 1])
                    work_sheet.write(column, 2, data[2][item - 1])
                    work_sheet.write(column, 3, data[3][item - 1])
                    work_sheet.write(column, 4, data[4][item - 1])
                    column = column + 1
                time.sleep(5)
        work_book.save('Douban_Movie.csv')
