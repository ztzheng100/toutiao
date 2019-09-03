#!usr/bin/env python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         test
# Description:
# Author:       zzt
# Date:         2019/7/29
#-------------------------------------------------------------------------------

import sys
# -*-coding:UTF-8-*-
# 引用selenium中的webdriver类

from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import json
from charpter13.Slider import Crack
from selenium.webdriver.common.keys import Keys
class Toutiao():
    def __init__(self):
        self.url = 'https://sso.toutiao.com/login/?service=https://mp.toutiao.com/sso_confirm/?redirect_url=/'
        #self.chrome_driver=''  #预留配置chrome_driver的路径
        self.driver = webdriver.Chrome()    # webdriver.Chrome(executable_path=self.chrome_driver)
        self.crack = Crack(self.driver)

    def login_toutiao(self,phone,password):
        """
       登录头条，保存cookies
       :return:
       """
        time.sleep(10)
        self.driver.get(self.url)
        print(self.driver.title)
        # # 移动鼠标到 手机位置点击
        ac = self.driver.find_element_by_id('login-type-account')
        ActionChains(self.driver).move_to_element(ac).click(ac).perform()
        # 输入账号密码
        self.driver.find_element_by_id('user-name').send_keys(phone)  # 头条用户名
        self.driver.find_element_by_id('password').send_keys(password)  # 头条密码
        time.sleep(5)
        # 点击登录按钮
        login = self.driver.find_element_by_id('bytedance-login-submit')
        ActionChains(self.driver).move_to_element(login).click(login).perform()
        time.sleep(10)
        #  获取cookies
        cookies = self.driver.get_cookies()
        cookies = json.dumps(cookies)
        # 将cookies保存到本地,也可以保存到数据库中
        with open(phone + '.txt', 'w') as f:
            f.write(cookies)
        f = open(phone + '.txt')
        cookie = f.read()
        cookie = json.loads(cookie)
        for i in cookie:
            self.driver.add_cookie(i)
        time.sleep(1)
        self.crack.slider_move()
        time.sleep(5)

    def send_video(self, title, video_path,tag_list):
        """
           发送小视频
           title  小视频的标题
           video_path  小视频的路径
           :param title:
           :return: 0 正常；1 视频重复上传失败；
           """
        # 转到发布界面
        time.sleep(5)
        video_url = 'https://mp.toutiao.com/profile_v3/xigua/upload-video'
        self.driver.get(video_url)
        time.sleep(10)
        #上传视频
        try:
            upload_video = self.driver.find_element_by_xpath("//*[@id='upload-manage']/div[4]/input")
        except:
            upload_video = self.driver.find_element_by_xpath("//*[@id='upload-manage']/div[3]/input")
            print("except=upload_video3")
        # print（upload_video.get_attribute('accept')）
        upload_video.send_keys(video_path)
        # 上传视频等待时间
        time.sleep(10)
        video = self.driver.find_element_by_xpath("//div[@class='upload-btn']/span")
        if video.text == '视频重复':
            print("视频重复="+video_path)
            self.driver.maximize_window()
            time.sleep(5)
            video_del = self.driver.find_element_by_xpath(
                "//*[@id='upload-manage']/div[2]/div[2]/div/div[1]/div[1]/div[1]/div/span[2]")
            #video_del.click()
            ActionChains(self.driver).move_to_element(video_del).click(video_del).perform()
            # alter 对话框处理
            time.sleep(10)
            video_sure = self.driver.find_element_by_xpath(
                "//*[@id='__CUSTOM_COMPONENT']/div/div/div/div[2]/div[3]/div[1]")
            video_sure.click()
            return 1
        # 标题
        title_con =  self.driver.find_element_by_xpath("//*[@id='upload-manage']/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[3]/div[2]/input")
        title_con.clear()
        title_con.send_keys(title)
        # 简介
        tag_str = ",".join(tag_list)
        tag_con = self.driver.find_element_by_xpath("//*[@id='upload-manage']/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[5]/div[2]/span[1]/textarea")
        tag_con.clear()
        tag_con.send_keys(tag_str)
        time.sleep(1)
        # 广告选中
        ad_mon = self.driver.find_element_by_xpath(
            "//div[@id='upload-manage']/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[3]/div[2]/label[1]/span")
        ad_mon.click()
        video_tag = self.driver.find_element_by_xpath(
            "//*[@id='react-select-2--value']/div[2]/input")
        ActionChains(self.driver).move_to_element(video_tag).click(video_tag).perform()
        for tag in tag_list:
            tag_str = tag + "\r\n \r\n"
            video_tag.send_keys(tag_str)
            time.sleep(1)
        video_send = self.driver.find_element_by_xpath("//*[@id='js-batch-footer-0']/div[1]")
        video_send.click()
        return 0

    def close_video(self):
        self.driver.close()




if __name__ == '__main__':
    # 选择浏览器
    toutiao = Toutiao()
    url_cur = ""
    url_cent = "https://mp.toutiao.com/profile_v3/index"
    while url_cur != url_cent:
        try:
            toutiao.login_toutiao('15917902851','zt131136')
        except Exception as e:
            pass
        url_cur=toutiao.driver.current_url
        print("url_cur="+url_cur)
    print("登录成功=" )
    time.sleep(5)
    res = toutiao.send_video("123","C:\\Users\\zzt\\Desktop\\辅导费12.mp4",["动漫","王宝强"])
    print(res)




