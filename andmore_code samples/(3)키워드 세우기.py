# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 09:19:36 2021

@author: RSN
"""


import pandas as pd

# 데이터 불러오기
data = pd.read_excel('data.xlsx', sheet_name='Sheet1')
print(data.head())
data.info()

data_copy = data.copy()

# na 포함된 row 제외: na 포함된 row의 index를 is_NaN에 저장한 후 이를 이용하여 데이터에서 제외
is_NaN = data_copy[data_copy['col_to_expand'].isnull()].index
data_copy_dropna = data_copy.drop(is_NaN)

# 단어 세우기: 중복된 아이디와 키워드 삭제
data_copy_dropna['연관어'] = data_copy_dropna['col_to_expand'].str.split(",")
data_copy_dropna_exp = data_copy_dropna.explode('연관어').drop_duplicates(subset=['unique_id', '연관어'], keep='last')

# 제외한 row 다시 넣기: 제외된 index가 저장된 is_NaN을 이용하여 데이터에서 해당 row 가져오기, 문장 세우고 중복 제거까지 모두 완료된 최종 데이터프레임에 붙여넣기
add_na_columns = data_copy[data_copy.index.isin(is_NaN)]
data_copy_dropna_exp = data_copy_dropna_exp.append(add_na_columns)

# 데이터 저장: 데이터가 너무 많아서 저장하는데 오래 걸린다면 필요한 컬럼만 따로 지정하기
with pd.ExcelWriter('save_data.xlsx') as writer:
    data_copy_dropna_exp.to_excel(writer) #최종 데이터 지정한 변수명[[필요한 컬럼들만 지정]].to_excel(writer)
