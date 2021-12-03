from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image
from collections import defaultdict

class SimpleGroupedColorFunc(object):
    """Create a color function object which assigns EXACT colors
       to certain words based on the color to words mapping
 
       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.
 
       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """
 
    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}
 
        self.default_color = default_color
 
    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)
    

# 클라우드 모양 맞출 파일(shape)과 데이터(data) 불러오기
shape = np.array(Image.open("000_oval2.jpg"))
data = pd.read_excel("data.xlsx", sheet_name="클라우드")
data.info()


# 브랜드 리스트 가져오고(brand) 필요한 연관어 그룹만 따로 저장하기(data_single) (한 브랜드/그룹만 그린다면 건너뛰어도 되는 부분)
brand = data['브랜드'].unique()[0] #unique (브랜드 열에서 각 브랜드 이름 한번만 가져오기), [n] (가져온 브랜드 리스트에서 n번째 브랜드 설정)
data_single = data[data['브랜드'] == brand] #위에 brand에 저장한 브랜드 이름으로 data의 브랜드 열에서 브랜드에 해당하는 연관어 그룹 따로 저장하기


# 각 연관어와 정보량끼리 짝 지어주기 (위의 그룹 따로 저장하는 부분 실행하지 않는다면 data_single은 초기에 불러온 원본 데이터 data로 변경)
single_dic = data_single.set_index('연관어')['정보량'].to_dict()


# '연관어:정보량' 으로 워드 클라우드 만들기 (그룹 따로 지정하는 부분 실행했다면 cj_dic, 안했다면 원본 데이터 data)
wc_beauty = WordCloud(font_path='C:/Users/RSN/anaconda3/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/CJ ONLYONE NEW title Bold.ttf', #폰트지정
             mask=shape, #위에 불러온 클라우드 모양 파일 (지정하지 않는다면 기본 배경에 동그랗게 그려짐)
             width=500, #이미지의 가로 크기
             height=500, #이미지의 세로 크기
             #relative_scaling=0.8, #정보량과 순위 함께 고려하여 글씨 크기 정하기
             max_font_size=130, #최대 폰트 크기
             min_font_size=15, #최소 폰트 크기
             #prefer_horizontal=5, #모든 단어 가로로 고정
             background_color='white').generate_from_frequencies(single_dic)  #배경 색


# 각 연관어 별로 지정해준 색끼리 그루핑하기
dic = data_single.groupby('색상')['연관어'].apply(list)


# 색상이 지정되지 않은 단어는 default_color로, 위에 그루핑해서 저장한 dic과 디폴트 색상 함수에 적
default_color = '#383838'
grouped_color_func = SimpleGroupedColorFunc(dic, default_color)


# 출력 확인
plt.figure(figsize=(8,8))
plt.imshow(wc_beauty.recolor(color_func=grouped_color_func))
plt.axis('off');


# 이미지 저장
fig = plt.figure(figsize=(100,100))
plt.imshow(wc_beauty.recolor(color_func=grouped_color_func), interpolation='bilinear')
plt.axis('off');
fig.savefig("save_data_{}.jpg".format(brand)) #위에 brand 변수에 저장한 이름이 {}에 자동으로 들어가도록