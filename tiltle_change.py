#!usr/bin/env python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         tiltle_change
# Description:  
# Author:       zzt
# Date:         2019/8/23
#-------------------------------------------------------------------------------

import sys
import random
from xpinyin import Pinyin
import re
class Title_con:
    def __init__(self,title):
        self.title=title

    def title_change(self):
        ran_str=""
        list_raw = self.title.split(":",1)
        if len(list_raw)==1:
            body = list_raw[0]
            name = ""
        else:
            name = list_raw[0]
            body = list_raw[1]

        l1 = re.split("\W+",body)
        len_num = len(l1)
        ran_list = [x for x in range(len_num)]
        random.shuffle(ran_list)
        print(l1)

        for i in ran_list:
            # print(l1[i])
            if l1[i] !='':
                ran_str=ran_str+l1[i]+','
        ran_str=ran_str[0:-1]+'!'
        if name != '':
            pin = Pinyin()
            name = pin.get_pinyin(name)
            ran_str=ran_str+'--'+name
        return ran_str
if __name__ == '__main__':
    title_con =Title_con("《海贼》: 被罗杰邀请入伙,冥王雷利: 一边玩去!")
    str = title_con.title_change()
    print(str)