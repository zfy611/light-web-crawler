#!/usr/bin/python3
# encoding=utf-8

"""该程序为示例程序：在马蜂窝景点中爬取的景点数据，并进行一定的数据分析。

project中为本项目编写的程序方法。

Args:
    FILE_PATH: 爬取数据保存路径
    LOCATIONS: 计划抓取图片的地区（需为准确的专有名词，即在马蜂窝中可直接搜索到）
    GET_LANDMARK_NUM: 计划在选定的地区抓取的景点数量
    DOWNLOAD_PIC_NUM: 每个景点抓取的图片数
    PROCESSING_POOL: 指定最大运行进程数

"""

import os
import sys
from multiprocessing import Pool

from selenium import webdriver

FILE_PATH = os.path.abspath('.')  # projects项目函数API地址，默认与示例程序同目录

sys.path.append(FILE_PATH + '/projects')
from projects import comments_analysis as cm
from projects import landmark_pic_crawler as lpc

# 参数配置
LOCATIONS = ['陕西', '北京', '安徽']  # 爬取地点
GET_LANDMARK_NUM = 5  # 爬取景点数
DOWNLOAD_PIC_NUM = 9  # 每个景点爬取图片数
PROCESSING_POOL = Pool(3)  # 最多同时运行进程数

# 图片抓取
def _pic_clawer():
    browser_obj = webdriver.Chrome()
    fail_download_locations = []  # 下载失败的地区
    # 循环下载
    for location in LOCATIONS:
        if not lpc.location_landmark_pic_download(
                browser_obj, location, GET_LANDMARK_NUM, DOWNLOAD_PIC_NUM, FILE_PATH + '/docs/pic'):
            print(location + "下载失败")
            fail_download_locations.append(location)
    # 输出下载失败的地区
    if len(fail_download_locations) > 0:
        print("下载失败地点：", end='')
        print(fail_download_locations)
    else:
        print("所有地点下载完成")
    browser_obj.quit()  # 退出浏览器


# 数据分析



PROCESSING_POOL.apply_async(_pic_clawer, args=())
PROCESSING_POOL.apply_async(cm.texts_analysis,
                            args=(FILE_PATH + '/docs/comments',
                                  FILE_PATH + '/projects/stopwords/stopwords.txt'))
PROCESSING_POOL.close()
PROCESSING_POOL.join()
print('示例程序运行完毕！')
