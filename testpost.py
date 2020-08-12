import requests
import unicodedata

from bs4 import BeautifulSoup
from qa.qa import QA


def get_body_content(domain, pageid):

    result = requests.get(f"https://{domain}/rest/api/content/{pageid}?expand=body.storage",
                          auth=('confluence', '186o73l7'))
    if result.status_code != 200:
        raise

    text = BeautifulSoup(result.json()['body']['storage']['value'], 'lxml').text
    text = unicodedata.normalize("NFKD", text)
    return text


domain = "confluence.julien.tech"
pageid = "65558"



question = 'How can I change the color of the text in confluence ?'
context = get_body_content(domain, pageid)
print (context)
qa = QA()
result = qa.predict(context, question)
print (result)
answer=result[0][0]['answer'][0]

start=context.find(answer)
end = start + len(answer)
html_answer=f'<p>{context[start-20:start]}</p><span style="background-color:#dfd;">{context[start:end]}</span><p>{context[end:end+20]}</p>'
print(html_answer)
#result = [{'id': '0', 'answer': ['some fun: Change the color of the text: Select the text, then choose a color from the color option in the editor tool bar.Add', 'some fun: Change the color of the text: Select the text,', 'some fun: Change the color of the text: Select the text, then choose a color from the color option', 'page.Have some fun: Change the color of the text: Select the text, then choose a color from the color option in the editor tool bar.Add', 'page.Have some fun: Change the color of the text: Select the text,', 'then choose a color from the color option in the editor tool bar', 'some fun: Change', 'choose a color from the color option in the editor tool bar', 'some fun: Change the color of the text:', 'fun: Change the color of the text: Select the text, then choose a color from the color option in the editor tool bar.Add', 'Select the text, then choose a color from the color option in the editor tool bar.Add', 'fun: Change the color of the text: Select the text,', 'Select the text,', 'page.Have some fun: Change the color of the text: Select the text, then choose a color from the color option', 'some fun: Change the color of the text: Select the text, then choose a color from the color', 'some fun: Change the color', 'some fun: Change the color of the text: Select the text, then choose a color', 'then choose a color from the color option', 'choose a color from the color option', 'page.Have some fun: Change']}], [{'id': '0', 'probability': [0.2183961740321435, 0.18970111426689418, 0.07324601672088768, 0.0667977000163684, 0.058021154352758106, 0.04944038172608587, 0.042850897031548076, 0.04048697569520287, 0.030014282325898797, 0.0299099369819806, 0.026166903884263744, 0.025980072216371407, 0.02272883600529087, 0.022402706796482874, 0.021226536150129607, 0.020486380100329327, 0.018870751025526725, 0.016581384919604734, 0.013578578983313778, 0.013106188228940129]}]

