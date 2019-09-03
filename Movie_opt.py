#!usr/bin/env python
# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Name:         Movie_opt
# Description:  
# Author:       zzt
# Date:         2019/8/23
# -------------------------------------------------------------------------------

import sys

from moviepy.editor import VideoFileClip, concatenate_videoclips



class Movie_opt:
    def __init__(self, in1="lightmv2.mp4", in2="0.mp4", out_title='动漫.mp4'):
        self.in1 = in1
        self.in2 = in2
        self.out_title = out_title

    def movie_con(self):
        clip1 = VideoFileClip(self.in1)
        clip2 = VideoFileClip(self.in2)
        # clip3 = VideoFileClip(self.out_title)
        print(clip1.size)
        print(clip1.size)
        finalclip = concatenate_videoclips([clip1, clip2],method='compose')
        finalclip.write_videofile(self.out_title)


if __name__ == '__main__':
    # 视频拼接
    movie_opt = Movie_opt(out_title="my_concatenate.mp4")
    movie_opt.movie_con()
    #
    # clip1 = VideoFileClip("0.mp4")
    # clip2 = VideoFileClip("lightmv2.mp4")
    #
    #
    # finalclip = concatenate_videoclips([clip2, clip1],method='compose')
    # finalclip.write_videofile("my_concatenate.mp4")
