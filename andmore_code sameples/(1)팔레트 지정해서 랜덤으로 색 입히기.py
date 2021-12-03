import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image


# 클라우드 모양 맞출 파일(shape)과 데이터(data) 불러오기
shape = np.array(Image.open("000_circle.jpg"))
data = pd.read_excel("data.xlsx", sheet_name="Sheet1")
data.info()


# 필요한 연관어 그룹만 따로 저장하기 (한 브랜드/그룹만 그린다면 건너뛰어도 되는 부분)
data_sns = data[data['그룹'] == 'SNS']


# 각 연관어와 정보량끼리 짝 지어주기 (위의 그룹 따로 저장하는 부분 실행하지 않는다면 data_cj는 초기에 불러온 원본 데이터 data로 변경)
dic = data_sns.set_index('연관어')['정보량'].to_dict()


# '연관어:정보량' 으로 워드 클라우드 만들기 (그룹 따로 지정하는 부분 실행했다면 cj_dic, 안했다면 원본 데이터 data)
wc = WordCloud(font_path='C:/Users/RSN/anaconda3/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/malgun.ttf', #폰트지정 (해당 경로에 원하는 폰트 파일 저장하고 폰트 지정)
             mask=shape, #위에 불러온 클라우드 모양 파일 (지정하지 않는다면 기본 배경에 동그랗게 그려짐)
             # width=1000, #이미지의 가로 크기
             # height=1000, #이미지의 세로 크기
             max_font_size=400, #최대 폰트 크기
             # min_font_size=15, #최소 폰트 크기 
             prefer_horizontal=5, #모든 글씨 가로로 고정
             colormap='Dark2', #지정한 팔레트 속에서 랜덤으로 색 입힘 (구글에 colormap 검색하면 다른 팔레트 코드 확인 가능)
             background_color='white').generate_from_frequencies(dic)  #배경 색


# 출력 확인
plt.figure(figsize=(8,8))
plt.imshow(wc_cj)
plt.axis("off");


# 이미지 저장
fig = plt.figure(figsize=(100,100))
plt.imshow(wc, interpolation='none')
plt.axis("off")
fig.savefig("save_data.jpg")