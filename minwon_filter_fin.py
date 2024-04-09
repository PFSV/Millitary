import pandas as pd
import requests
import re

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
        'app_id': '##########################################',
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

data = pd.read_excel("finlist_filtered.xlsx",engine="openpyxl")
df = pd.read_excel("minwon_valid copy.xlsx",engine= "openpyxl")
data = data[0]

resultlist = []

for i in data[0:4]:
    i = i.split("&")
    big = i[0]
    mid = i[1]
    small = i[2]
    minor = i[3]
    title = i[4]
    text = i[5]
    prompt = "너는 9단어 내로 '내용에 있는 단어들로' 요약을 참 잘해. 다음 민원 내용의 핵심을 분류를 참고해서 '반드시 내용에 있는 단어들로' 9단어 내로 요약해줘. 민원 분류는 {0} > {1} > {2} > {3}이야. \
    제목은 {4}이고 내용은 {5}.".format(big,mid,small,minor,title,text)
    result = gptStream(prompt)
    resultlist.append(result) 
    print("제목은: {0}".format(title))
    print("내용은: {0}".format(text))
    print("요약은 : {0}".format(result))
    print("\n")

df["요약 내용"] = resultlist
df.to_excel("fin_minwon_testing.xlsx",index=False)