#!usr/bin/env python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         viodes
# Description:  m3u8视频下载
# Author:       zzt
# Date:         2019/7/25
#-------------------------------------------------------------------------------


import sys
import os
from glob import glob
import requests
import traceback

#reload(sys)
#sys.setdefaultencoding("utf-8")
file_path=os.getcwd()

#获取需要转换的路径
def get_user_path(argv_dir):
    if os.path.isdir(argv_dir):
        return argv_dir
    elif os.path.isabs(argv_dir):
        return argv_dir
    else:
        return False

#对转换的TS文件进行排序
def get_sorted_ts(user_path):
    ts_list = glob(os.path.join(user_path, '*.ts'))
    boxer = []
    for ts in ts_list:
        if os.path.exists(ts):
            # print(os.path.splitext(os.path.basename(ts)))
            file, _ = os.path.splitext(os.path.basename(ts))
            print(file)
            boxer.append(file)
            # boxer.append(int(file))
    boxer.sort()
    print(boxer)
    return boxer

#文件合并

def convert_m3u8(file_path,boxer,o_file_name):
    print(u"开始拼接视频")
    new_path = file_path + "/" + u"视频"
    try:
        os.chdir(new_path)
    except Exception as e:
        os.mkdir(new_path)
    tmp = []
    for ts in boxer:
        print(ts)
        tmp.append(str(ts) + '.ts')
        cmd_str = '+'.join(tmp)
    exec_str = "copy /b " + cmd_str + ' ' + o_file_name
    print("copy /b " + cmd_str + ' ' + o_file_name)
    os.chdir(user_path)
    os.system(exec_str)
    print("go home path")
    import shutil
    shutil.move(o_file_name, new_path + "/" + o_file_name)
    os.chdir(file_path)



# 功能：爬取m3u8格式的视频
# 检查存储路径是否正常
def check_path(_path):
    # 判断存储路径是否存在
    if os.path.isdir(_path) or os.path.isabs(_path):
        # 判断存储路径是否为空
        if not os.listdir(_path):
            return _path
        else:
            print(u'>>>[-] 目标文件不为空，将清空目标文件，是否更换路径？')
            flag = input('>>>[*] Yes:1 No:2 \n>>>[+] [2]')
            try:
                if flag == '1':
                    _path = input((u'>>>[+] 请输入目标文件路径。\n>>>[+] ').encode('gbk'))
                    check_path(_path)
                else:
                    # 清空存储路径
                    os.system('rd /S /Q ' + _path)
                    os.system('mkdir ' + _path)
                    return _path
            except Exception as e:
                print(e)
                exit(0)
    else:
        os.makedirs(_path)
        return _path

# 获取ts视频的爬取位置
def get_url(_url, _path):
    all_url = _url.split('/')
    url_pre = '/'.join(all_url[:-1]) + '/'
    url_next = all_url[-1]
    if '?'.find(url_next):
        url_next="test.m3u8"
    os.chdir(_path)
    # 获取m3u8文件
    m3u8_txt = requests.get(_url, headers={'Connection': 'close'})
    with open(url_next, 'wb') as m3u8_content:
        m3u8_content.write(m3u8_txt.content)
        # 提取ts视频的url
        movies_url = []
        _urls = open(url_next, 'r')
        for line in _urls.readlines():
            if '.ts' in line:
                movies_url.append(url_pre + line[:-1])
            else:
                continue
        _urls.close()
    return movies_url

# 爬取ts视频
def download_movie(num,movie_url, _path):
    os.chdir(_path)
    print(u'>>>[+] 第{}个视频 downloading...'.format(num))
    print('-' * 60)
    error_get = []
    for _url in movie_url:
        # ts视频的名称
        movie_name = _url.split('/')[-1][-6:]
        movie_name1 = _url.split('_')[-1][-6:]
        if len(str(movie_name1)) <= 4:
            movie_name1 = "00" + str(movie_name1)
        elif len(str(movie_name1)) <= 5:
            movie_name1 = "0" + str(movie_name1)
        else:
            movie_name1 = str(movie_name1)
        try:
            # 'Connection':'close' 防止请求端口占用
            # timeout=30 防止请求时间超长连接
            movie = requests.get(_url, headers={'Connection': 'close'}, timeout=60)
            with open(movie_name1, 'wb') as movie_content:
                movie_content.writelines(movie)
                print(u'>>>[+] 视频片段 ' + movie_name1 + u' 下载完成')
        # 捕获异常，记录失败请求
        except:
            error_get.append(_url)
            continue
    # 如果没有不成功的请求就结束
    if error_get:
        print(u'共有%d个请求失败' % len(error_get))
        print('-' * 60)
        download_movie(error_get, _path)
    else:
        print('>>>[+] Download successfully!!!')


#url=["http://video.renrenjiang.cn/record/alilive/7684990805-1512186274.m3u8"]
url=["https://v-acfun.com/20180809/6821_96aa0dac/1000k/hls/index.m3u8"]

if __name__ == '__main__':
    try:
        # _url = raw_input(unicode('>>>[+] 请输入指定的[.m3u8]目标URL。\n>>>[+] ').encode('gbk'))
        # _path = raw_input(unicode('>>>[+] 请输入存储目标文件路径。\n>>>[+] ').encode('gbk'))
        for i in range(len(url)):
            _url = url[i]
            _path = os.getcwd() + "\\" + "ts" + str(i + 5)
            try:
                os.chdir(_path)
            except Exception as e:
                os.mkdir(_path)
            storage_path = check_path(_path)
            movie_url = get_url(_url, storage_path)
            download_movie(i + 1, movie_url, storage_path)  # 下载视频
            user_path = _path
            o_file_name = str(i + 5) + ".mp4"
            boxer = get_sorted_ts(user_path)
            convert_m3u8(file_path, boxer, o_file_name)  # 拼接视频
    except Exception as e:
        print(e)
        print(sys._getframe().f_lineno, 'traceback.print_exc():',traceback.print_exc())
        print(sys._getframe().f_lineno, 'traceback.format_exc():\n%s' % traceback.format_exc())