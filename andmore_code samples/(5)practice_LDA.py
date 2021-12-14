# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 16:08:13 2021

@author: RSN
"""

#LDA
#문서의 집합에서 토픽을 찾아내는 프로세스 (문서 주제 알아내기); 토픽들의 혼합으로 구성되어 있는 문서들, 토픽 확률 분포에 기반하여 단어들을 생성
#빈도수 기반의 BoW의 행렬 DTM 또는 TF-IDF 행렬 입력, 단어의 순서 신경쓰지 않음

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from gensim import corpora, models
import gensim
import warnings
warnings.filterwarnings(action="ignore")
import matplotlib.pyplot as plt
from gensim.models import CoherenceModel
import pyLDAvis
import pyLDAvis.gensim_models
from wordcloud import WordCloud
import pickle

#encoding 형식에 맞춰서 파일 불러오기
data = pd.read_csv("test.csv",encoding="CP949")

#데이터 복사하기
df = data.copy()

#텍스트 전처리: 분석할 연관어가 있는 컬럼에서 로우를 하나씩 불러와 ','로 분리한 다음 한 글자 연관어를 제외한 나머지 연관어 새로운 list 변수에 저장
d = {'추천해요': '추천', '만족': '만족스럽다', '올리브영 추천템': '올리브영 추천', '스킨': '스킨케어', '케어': '스킨케어', '괜찮': '괜찮다'}
lis = ['오늘', '가지', '사실', '생기', '걔속', '이상', '참고', '모두', '하루', '우리', '마지막', '수도', '동안', 'Olive', '서울특별시', '계속', '별로다', '남아', '차이', '심한', '높다']
data_list = []
for x in df['세우기'].astype(str):
    x = x.split(',')
    x = [word for word in x if word not in lis] #특정 단어를 아예 제외하고 싶을 때
    x = [word if word not in d.keys() else d.get(word) for word in x] #특정 단어를 아예 다른 단어로 바꾸고 싶을 때
    data_list.append([y for y in x if not len(y) == 1])


#단어 -> 숫자: 단어 정수 인코딩과 각 문서에서 단어의 빈도수 (word_id, word_frequency)
dictionary = corpora.Dictionary(data_list)
dictionary.filter_extremes(no_below = 20) #20회 이하로 등장한 단어는 삭제
corpus = [dictionary.doc2bow(text) for text in data_list]

#topic 수 선정: 일정 topic 수로 모델링하여 coherence와 perplexity score 시각화
coherence_values = [] #Coherence 값이 높을수록 좋다

for i in range(2,15):
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = i, id2word=dictionary)
    coherence_model_lda = CoherenceModel(model = ldamodel, texts = data_list, dictionary = dictionary, topn=10)
    coherence_lda = coherence_model_lda.get_coherence()
    coherence_values.append(coherence_lda)
    
x = range(2,15)    
plt.plot(x, coherence_values)
plt.xlabel('number of topics')
plt.ylabel('coherence score') # coherence score가 가장 높은 값을 보이는 구간 찾아 최적화된 토픽 개수 선정
plt.show()

perplexity_values = [] #Perplexity 값이 낮을수록 좋다
for i in range(2,15):
    ldamodel=gensim.models.ldamodel.LdaModel(corpus, num_topics = i, id2word = dictionary)
    perplexity_values.append(ldamodel.log_perplexity(corpus))

x = range(2,15)
plt.plot(x, perplexity_values)
plt.xlabel('number of topics')
plt.ylabel('perplexity score') # perplexity score가 가장 낮은 값을 보이는 구간 찾아 최적화된 토픽 개수 선정
plt.show()

#lda 최종 모델링: coherence와 perplexity 시각화 결과물을 바탕으로 최적의 topic 수(num_topics)를 결정하여 최종 모델링
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 3, id2word = dictionary, alpha=0.01, eta=0.1, passes=30)
ldamodel.print_topics(num_words=10) #모델 확인

#최종 lda 모델 시각화: 좌표 및 연관어 리스트(람다 조절)
pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim_models.prepare(ldamodel, corpus, dictionary)
pyLDAvis.save_html(vis, 'test.html')

##최종 lda 모델 시각화: 워드클라우드
for t in range(ldamodel.num_topics):
  plt.figure()
  plt.imshow(WordCloud(font_path='C:/Users/RSN/anaconda3/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/malgun.ttf',
                       colormap='Dark2',
                       background_color='white').fit_words(dict(ldamodel.show_topic(t, 30))))
  plt.axis("off");

#모델링에 사용된 변수 저장하기: corpus, dictionary, lda model 저장
with open('/content/drive/MyDrive/Colab Notebooks/출산_2020_corpus.pickle', 'wb') as fw:
  pickle.dump(corpus, fw)
dictionary.save('/content/drive/MyDrive/Colab Notebooks/출산_2020_dictionary.gensim')
ldamodel.save('/content/drive/MyDrive/Colab Notebooks/출산_2020_ldamodel.gensim')

#문서 별로 토픽 분포 보기: 엑셀 시트로 저장하기
def make_topictable_per_doc(ldamodel, corpus):
    topic_table = pd.DataFrame()

    # 몇 번째 문서인지를 의미하는 문서 번호와 해당 문서의 토픽 비중을 한 줄씩 꺼내온다.
    for i, topic_list in enumerate(ldamodel[corpus]):
        doc = topic_list[0] if ldamodel.per_word_topics else topic_list            
        doc = sorted(doc, key=lambda x: (x[1]), reverse=True)
        # 각 문서에 대해서 비중이 높은 토픽순으로 토픽을 정렬한다.
        # EX) 정렬 전 0번 문서 : (2번 토픽, 48.5%), (8번 토픽, 25%), (10번 토픽, 5%), (12번 토픽, 21.5%), 
        # Ex) 정렬 후 0번 문서 : (2번 토픽, 48.5%), (8번 토픽, 25%), (12번 토픽, 21.5%), (10번 토픽, 5%)
        # 48 > 25 > 21 > 5 순으로 정렬이 된 것.

        # 모든 문서에 대해서 각각 아래를 수행
        for j, (topic_num, prop_topic) in enumerate(doc): #  몇 번 토픽인지와 비중을 나눠서 저장한다.
            if j == 0:  # 정렬을 한 상태이므로 가장 앞에 있는 것이 가장 비중이 높은 토픽
                topic_table = topic_table.append(pd.Series([int(topic_num), round(prop_topic,4), topic_list]), ignore_index=True)
                # 가장 비중이 높은 토픽과, 가장 비중이 높은 토픽의 비중과, 전체 토픽의 비중을 저장한다.
            else:
                break
    return(topic_table)

topictable = make_topictable_per_doc(ldamodel, corpus)
topictable = topictable.reset_index()
topictable.columns = ['문서 번호', '가장 비중이 높은 토픽', '가장 높은 토픽의 비중', '각 토픽의 비중']
topictable.to_csv('test.csv')