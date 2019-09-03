#!usr/bin/env python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         start
# Description:  
# Author:       zzt
# Date:         2019/8/23
#-------------------------------------------------------------------------------

import os
import time
from Movie_opt import Movie_opt
from Uc_viodes import Uc_get
from Toutiao import Toutiao

if __name__ == '__main__':
    phone ="123456"
    password = "123456"
    out_title = "my_concatenate.mp4"
    url_cent = "https://mp.toutiao.com/profile_v3/index"
    uc_url = "http://iflow.uczzd.cn/iflow/api/v1/article/3252968475747632673/related_video?app=uc-iflow&cid=10012&count=" \
          "3&his_size=26&req_number=8&enable_ad=1&ad_extra=AAMXR2M9zDR58pt%2FPE%2F0J3S%2B&uc_param_str=dnnivebichfrmintcpgidsudsvmedizbssnw&dn=" \
          "24649292336-0dd3910c&nn=AAS6DOPmwycJ2UY%2BpHvQ2V1MV6W9aqVklzhRKUnwV8fliQ%3D%3D&ve=" \
          "12.2.8.1008&bi=35030&ch=yzappstore%40&fr=android&mi=MI 8&nt=2&pc=AAQ%2FJDdbUVTj%2FurM6xuCLCy3x8NPLm6zLsN0iwQlhwuue%2FY" \
          "%2F7K3uw%2F%2Fch%2B3cAKlMQaPfA4YTVVgk%2FwBdsqerGt7c&gp=&ut=AARJTWVH%2BiO4hb2TbMyJS8%2FWrlDaX5Xdc404XYSj2skM6Q%3D%3D&ai=&sv=" \
          "ucrelease&me=AAQ1LnyQXnPpxzZbEAAeJ6nc&di=cb214aac20a097ad&zb=00000&ss=1080x2029&nw=WIFI&ab_tag=1934B2;1917A2;1878D2;1728A2;1794" \
          "C2;1918A2;&zb=00000&puser=0&ressc=44"
    uc_get = Uc_get(uc_url)
    list_tt = []
    while not list_tt :
        list_tt = uc_get.get_json()
    print(list_tt[0])
    uc_get.download(list_tt[0]['url_Html'], '0.mp4')
    time.sleep(2)
    movie_opt = Movie_opt(out_title=out_title)
    movie_opt.movie_con()

    toutiao = Toutiao()
    url_cur = ""
    while url_cur != url_cent:
        try:
            toutiao.login_toutiao(phone, password)
        except Exception as e:
            pass
        url_cur = toutiao.driver.current_url
        print("url_cur=" + url_cur)
    print("登录成功=")
    time.sleep(5)
    path_cen =os.path.join(os.getcwd(),out_title)
    res = toutiao.send_video(list_tt[0]['title'], path_cen,list_tt[0]['merge_tags'])
    print(res)
    # for i in range(3):
    #     uc_get = Uc_get(uc_url)
    #     list_tt = []
    #     while not list_tt:
    #         list_tt = uc_get.get_json()
    #     print(list_tt[0])
    #     uc_get.download(list_tt[0]['url_Html'], '0.mp4')
    #     time.sleep(2)
    #     movie_opt = Movie_opt(out_title=out_title)
    #     movie_opt.movie_con()
    #     res = toutiao.send_video(list_tt[0]['title'], path_cen, list_tt[0]['merge_tags'])
    #     print(res)
    time.sleep(20)
    toutiao.close_video()

