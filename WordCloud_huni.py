# -*- coding:utf-8 -*-
'''
워드클라우드 함수
작성: 성지훈

v1. 210822
- 과학소양논문에서 사용했던 워드클라우드 코드 사용
'''
import re, time, os, datetime, pickle
import pandas as pd
import numpy as np
from sys import platform

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

if 'ind' in platform: # for window
    plt.rc("font",family="Malgun Gothic")
elif 'darwin' in platform: # for mac
    plt.rc('font', family='AppleGothic') 
    font_path= '/System/Library/Fonts/Supplemental/AppleGothic.ttf'

from tqdm.notebook import tqdm
tqdm.pandas()



class Generate_WC:
    def __init__(self, title, txt, tagger, wd_limit):
        self.title = title
        self.txt = txt
        self.wd_limit = wd_limit
        self.tagger = tagger

    def mec(self, spword, save_directory):
        print('This Class built in 2021.08.22')
        if 'ind' in platform: # for window
            from eunjeon import Mecab 
            tagger = Mecab()
        elif 'darwin' in platform: # for mac
            from konlpy.tag import Mecab
            tagger = Mecab()
        # assert len(self.txt) == 1, print('Input Shape error: ', len(self.txt))
        
        freq_dic={}
        for each_respose in tqdm(self.txt): # txt: 2D list, (each elements is string)
            assert type(each_respose) == str , print('Input String type error: ', type(each_respose))    
            temp = tagger.nouns(each_respose) # 여기는 이미 클리닝이 되어 있으니까

            for word in temp:
                if word not in spword:
                    if word in freq_dic.keys():
                            freq_dic[word] += 1
                    elif word not in freq_dic.keys():
                            freq_dic[word] = 1  

        filtered_count_tuples = sorted(freq_dic.items(), key=lambda x: x[1], reverse=True) # count 수에 따라 내림차순으로 정렬하여 튜플로 저장
        filtered_count_tuples = filtered_count_tuples[:self.wd_limit] 
        twice_filtered_count = {k: v for k, v in filtered_count_tuples}

### gen WC
        wc = WordCloud(background_color='white', font_path=font_path, colormap=cm.winter)
        wc.generate_from_frequencies(twice_filtered_count)
        plt.figure(figsize=(6,6), dpi=600)
        plt.imshow(wc, 
                #    cmap=plt.cm.gray,
                        interpolation='bilinear')
        plt.title(f'\n{self.title}\n')

        plt.axis("off")
        plt.savefig(f'./{save_directory}/wordcloud_{self.title}.png',
                        transparent=False,
                        dpi=800)
        plt.show()
