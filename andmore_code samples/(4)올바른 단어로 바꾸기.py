# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 15:43:25 2021

@author: RSN
"""


import pandas as pd

# 단어 세우기 필요한 데이터 불러오기
data = pd.read_excel('data.xlsx', sheet_name='로우 데이터')
print(data.head())
data.info()
df = data.copy()

# na 포함된 row 제외: na 포함된 row의 index를 is_NaN에 저장한 후 이를 이용하여 데이터에서 제외
is_NaN = df[df['브랜드 연관어'].isnull()].index
df = df.drop(is_NaN)

# 단어 세우기: 중복된 아이디와 키워드 삭제
df['패턴 구문'] = df['브랜드 연관어'].str.split(",")
df_exp = df.explode('패턴 구문').drop_duplicates()

# 브랜드별 대표단어와 분류 리스트 불러오기
sort = pd.read_excel('data2.xlsx', sheet_name='Sheet1')
sort.info()

# df_exp 기준으로 sort와 공통으로 있는 컬럼 '패턴 구문'을 이용하여 데이터프레임 합치기
df_final = df_exp.merge(sort, how='left', on='패턴 구문')
df_final = df_final.drop_duplicates(subset=['문서번호', '대표단어'], keep='last')


with pd.ExcelWriter('save_data.xlsx') as writer:
    df_final[['col_to_save']].to_excel(writer)