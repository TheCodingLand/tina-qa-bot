
import pandas as pd

from bottle import run, post, request
from atlassian import Confluence
import json
import requests
import unicodedata
from bs4 import BeautifulSoup
from qa.qa import QA
import os
DOMAIN = os.getenv("CONFLUENCE_URL", "confluence.ctg.lu")
#pageid = "65558"

qa = QA()

def search_articles(question):
    question= question.replace("'", " ")
    confluence = Confluence(url='https://confluence.ctg.lu', username='confluence_rc_bot', password='B186o73l7')
    cql_query=f"type=page and space in (DEV) and text ~ '{question}'"

    articles = confluence.cql(cql_query, start=0, limit=2, expand=None, include_archived_spaces=None, excerpt=True)
    page = articles['results'][0]['content']
    
    page_content = confluence.get_page_by_id(page['id'], expand='body.view', status=None, version=None)
    #print (page_content['body']['view']['value'])
    return page_content['title'], page_content['body']['view']['value']


def get_body_content(t):

    text = BeautifulSoup(t, 'lxml').text
    text = unicodedata.normalize("NFKD", text)
    
    return text

def qa_prediction(question,context):
    result = qa.predict(context, question)
    answer=result[0][0]['answer'][0]

    start=context.find(answer)
    end = start + len(answer)
    html_answer=f'<p>{context[start-20:start]}</p><span style="background-color:#dfd;">{context[start:end]}</span><p>{context[end:end+20]}</p>'
    print(html_answer)
    return { "context": context, "question" : question, "start" : start, "end": end, "html" :html_answer, "link": "test"}




@post('/predict')
def predict():
    msg = json.loads(request.body.read()) # get the reques parameters  
    print(msg)
    question = msg['question'] #we get a keyerror if the model is not loaded in memory
    title,article = search_articles(question)
    context = get_body_content(article)
    result = qa_prediction(question, context)
    print (result)
    return result


run(host='0.0.0.0', port=8080, debug=True)






   




