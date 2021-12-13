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
is_NaN = df[df['col_to_expand'].isnull()].index
df = df.drop(is_NaN)

# 단어 세우기: 중복된 아이디와 키워드 삭제
df['패턴 구문'] = df['col_to_expand'].str.split(",")
df_exp = df.explode('패턴 구문').drop_duplicates()

# 브랜드별 대표단어 리스트(group), 브랜드별 편리,건강,즐거움 구분 리스트(sort) 불러오기
group = pd.read_excel('data2.xlsx', sheet_name='Sheet1')
sort = pd.read_excel('data3.xlsx', sheet_name='Sheet1')
print(group.head())
group.info()
sort.info()

# group과 sort에 동시에 존재하는 컬럼(패턴 구문)을 인덱스로 기준을 잡고 각 값에 해당하는 대표단어 값을 sort에 넣기
sort = sort.join(group.set_index('패턴 구문')['대표단어'], on='패턴 구문')
sort = sort.drop_duplicates()

df_exp = df_exp.join(group.set_index('패턴 구문')['대표단어'], on='패턴 구문')
df_final = df_exp.drop_duplicates(subset=['문서번호', '대표단어'], keep='last')

df_final = df_final.join(sort.set_index('대표단어')['sort'], on='대표단어')
df_final = df_final.drop_duplicates(subset=['문서번호', '대표단어'], keep='last')
print(df_final.head)
df_final.info()

with pd.ExcelWriter('save_data.xlsx') as writer:
    df_final[['col_to_save']].to_excel(writer)
    

brand_sort = pd.read_excel('data4.xlsx', sheet_name='Sheet1')

brand_cloud = pd.read_excel('data5.xlsx', sheet_name='Sheet1')
brand_cloud = brand_cloud.join(brand_sort.set_index('패턴 구문')['sort'], on='패턴 구문')
brand_cloud.to_excel('save_data.xlsx')