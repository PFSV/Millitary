import pandas as pd
import requests
import re


data = pd.read_excel("######.xlsx",engine= "openpyxl")

minwon = data['민원내용']
title = data["제목"]

corpus = []
for i,j in zip(minwon,title):
    i = i.replace("*","")
    i = i.replace("/","")
    corpus.append(i)
    
def regex(text):
    p = re.compile('"content":.*')
    llist = p.findall(response.text)
    newstring = ""
    for i in llist:
        korean_text = re.search(r'content":"(.*?)"', i).group(1)
        newstring += korean_text
    return newstring

def gptStream(question):

    headers = {
        'content-type': 'application/json'
    }

    reqData = {
        'app_id': '#####################################',
        'name': 'gpt4_stream',
        'item': [
            'gpt4-stream'
        ],
        'param': [
            {
                'model': 'gpt-4',
                'messages': [
                    {
                        'role': 'user',
                        'content': question
                    }
                ],
                'stream': True
            }
        ]
    }
    global response
    response = requests.post('https://norchestra-stg.maum.ai/harmonize/dosmart', json=reqData, headers=headers)

    return regex(response.text).replace("\\n","\n")

resultlist= []
for i in corpus:
    print("원문: "+i)
    if len(i)<10:
        result1 = i
    else:
        result1 = gptStream(i+"의도가 담긴 부분을 '있는 그대로' 토큰에서 잘라서 알려줘. 10단어 이내로, 형식은 반드시 띄어쓰기로 나열로 해줘")
    resultlist.append(result1)
    print("요약 결과: "+result1)
    print("\n")
    
data["키워드 추출"] = resultlist

data.to_excel("keyword_minwon.xlsx",index = False)
