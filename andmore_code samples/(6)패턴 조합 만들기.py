# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 13:34:58 2021

@author: RSN
"""

import pandas as pd

# 데이터 불러오기
df = pd.read_excel('sample.xlsx')
df.head()
data = df.copy() # df 변수명에 불러온 데이터 그대로 data 변수에 복사하기 

# 각 서비스별 감성 조합
sentiment = []
for each in data['서비스'].dropna().astype(str):
    sentiment.append(each + " " + data['긍정감성'].dropna().astype(str))
    sentiment_df = pd.concat([i for i in sentiment], ignore_index=True)
    
# 각 서비스 패턴별 감성 패턴 조합
sentiment_combination = []
for each in data['서비스 패턴'].dropna().astype(str):
    sentiment_combination.append(each + data['긍정감성 패턴'].dropna().astype(str))
    sentiment_combination_df = pd.concat([i for i in sentiment_combination], ignore_index=True)
    
# 전체 서비스 조합과 서비스 패턴 조합 하나의 프레임에 합치기, 컬럼 이름 바꿔주기
new_df = pd.concat([sentiment_df, sentiment_combination_df], axis=1)
new_df.rename(columns={'긍정감성': '서비스 조합', '긍정감성 패턴': '서비스 조합 패턴'})

# 최종 분석 패턴 만들기
fin_combi = []
for pattern in sentiment_combination_df:
    num = pattern.count(',') * 2
    fin_combi.append("[N,A,{}]({})".format(num, pattern))
    
# 서비스 조합과 서비스 조합 패턴 합친 테이블에 최종 분석 패턴 붙여넣기
new_df['최종'] = fin_combi
new_df.head() # 데이터 확인

# 데이터프레임 저장하기
new_df.to_excel('sample_result.xlsx')
