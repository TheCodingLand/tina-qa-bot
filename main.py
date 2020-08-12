
import pandas as pd

from bottle import run, post, request
import json
import requests
import unicodedata
from bs4 import BeautifulSoup
from qa.qa import QA
DOMAIN = os.getenv("CONFLUENCE_URL", "confluence.ctg.lu")
#pageid = "65558"

def get_body_content(pageid):

    result = requests.get(f"https://{DOMAIN}/rest/api/content/{pageid}?expand=body.storage",
                          auth=('confluence', '186o73l7'))
    if result.status_code != 200:
        raise

    text = BeautifulSoup(result.json()['body']['storage']['value'], 'lxml').text
    text = unicodedata.normalize("NFKD", text)
    return text

def qa_prediction(question,context):
    result = qa.predict(context, question)
    top_answer=result[0][0]['answer'][0]

    start=context.find(answer)
    end = start + len(answer)
    html_answer=f'<p>{context[start-20:start]}</p><span style="background-color:#dfd;">{context[start:end]}</span><p>{context[end:end+20]}</p>'
    return { "context": context, "question" : question, "start" : start, "end": end, "html" :html_answer}

@post('/predict')
def predict():
    msg = json.loads(request.body.read()) # get the reques parameters 
    
    question = loaded_models[msg['question']] #we get a keyerror if the model is not loaded in memory
    pageid = loaded_models[msg['pageid']] #we get a keyerror if the model is not loaded in memory
    context = get_body_content(pageid)
    result = qa_prediction(question, context)
    return result


run(host='0.0.0.0', port=8080, debug=True)






   




