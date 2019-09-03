#!usr/bin/env python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         test2
# Description:
# Author:       zzt
# Date:         2019/7/29
#-------------------------------------------------------------------------------
import requests

import json
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import requests
from urllib.request import urlretrieve
from tiltle_change import Title_con

class Uc_get():
    def __init__(self,url):
        self.url=url
        self.video_list=[]

    def get_json(self):
        # 发送请求，获取响应结果
        self.video_list = []
        response = requests.get(url=self.url)
        text = response.text
        # 将响应内容转换为Json对象
        jsonobj = json.loads(text)
        # 从Json对象获取想要的内容

        for i in range(3):
            video_dict = {}
            video_dict['title'] = Title_con(jsonobj["data"]['articles'][i]['title']).title_change()
            video_dict['name'] = jsonobj["data"]['articles'][i]['wm_author']['name']
            video_dict['content_length'] = jsonobj["data"]['articles'][i]['content_length']
            video_dict['url'] = jsonobj["data"]['articles'][i]['url']
            video_dict['url_Html'] = self.getHtml(video_dict['url'])

            video_dict['merge_tags'] = jsonobj["data"]['articles'][i]['merge_tags']
            # print(video_dict['name'])
            # print(video_dict['merge_tags'])
            print(video_dict['url_Html'])
            if video_dict['url_Html'] != "":
                if video_dict['title'].find("动漫" )>0: #str1.find(str2)
                    self.video_list.append(video_dict)
                else:
                    for tag in  video_dict['merge_tags']:
                        if tag.find("动漫")>0:
                            self.video_list.append(video_dict)
                            break
        print("json 获取成功")
        #print(self.video_list)
        return self.video_list

    def getHtml(slef,url, waittime=2):
        '''
        用于获取由加载生产的url视频地址
        :param url:
        :param waittime:
        :return:
        '''
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(chrome_options=chrome_options)
       # browser = webdriver.Chrome('chromedriver')
        browser.get(url)
        time.sleep(waittime)
        try:
            video_con = WebDriverWait(browser, 5).until(lambda b: browser.find_element_by_xpath("//*[@id='wemedia']/div[2]/div/div[1]/video"))
            # video_con = browser.find_element_by_xpath("//*[@id='wemedia']/div[2]/div/div[1]/video")
            video_url = video_con.get_attribute("src")
        except :
            video_url =""
       # print(video_url)
        browser.quit()
        return video_url
    def Schedule(self, a, b, c):
        """
        进度条
        :param a:
        :param b:
        :param c:
        :return:
        """
        per = 100.0 * a * b / c
        if per > 100:
            per = 1
        print("  " + "%.2f%% 已经下载的大小:%ld 文件大小:%ld" % (per, a * b, c) + '\r')

    def download(self,url,filename):

        try:
            print("\"" + filename + "\"" + "已经开始下载")
            urlretrieve(url, filename, reporthook=self.Schedule)
            print("\"" + filename + "\"" + "已经下载完成")
        except Exception as e:
            print(e)





if __name__ == '__main__':
    url = "http://iflow.uczzd.cn/iflow/api/v1/article/3252968475747632673/related_video?app=uc-iflow&cid=10012&count=" \
          "3&his_size=26&req_number=8&enable_ad=1&ad_extra=AAMXR2M9zDR58pt%2FPE%2F0J3S%2B&uc_param_str=dnnivebichfrmintcpgidsudsvmedizbssnw&dn=" \
          "24649292336-0dd3910c&nn=AAS6DOPmwycJ2UY%2BpHvQ2V1MV6W9aqVklzhRKUnwV8fliQ%3D%3D&ve=" \
          "12.2.8.1008&bi=35030&ch=yzappstore%40&fr=android&mi=MI 8&nt=2&pc=AAQ%2FJDdbUVTj%2FurM6xuCLCy3x8NPLm6zLsN0iwQlhwuue%2FY" \
          "%2F7K3uw%2F%2Fch%2B3cAKlMQaPfA4YTVVgk%2FwBdsqerGt7c&gp=&ut=AARJTWVH%2BiO4hb2TbMyJS8%2FWrlDaX5Xdc404XYSj2skM6Q%3D%3D&ai=&sv=" \
          "ucrelease&me=AAQ1LnyQXnPpxzZbEAAeJ6nc&di=cb214aac20a097ad&zb=00000&ss=1080x2029&nw=WIFI&ab_tag=1934B2;1917A2;1878D2;1728A2;1794" \
          "C2;1918A2;&zb=00000&puser=0&ressc=44"
    uc_get = Uc_get(url)
    list_tt = uc_get.get_json()
    print(list_tt[0])
    uc_get.download(list_tt[0]['url_Html'],'0.mp4')


