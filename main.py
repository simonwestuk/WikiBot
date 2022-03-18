import bs4 as bsoup
import urllib.request
import re
import requests
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
nltk.download('punkt')

topic = input("What is the topic we are discussing today?")
url = 'https://en.wikipedia.org/wiki/' + topic.replace(' ', '_')
get = requests.get(url)

if get.status_code == 200:
  data = urllib.request.urlopen(url).read()
  text = bsoup.BeautifulSoup(data, "html.parser").find_all('p')
  
  corpus = ''
  
  for t in text:
      corpus += t.text.lower()
  
  corpus_new = re.sub("[[].*[]]", "", corpus)
  
  sents = nltk.sent_tokenize(corpus_new)
  sents = list(filter(None,sents))
else:
  sents = ['Teach me something!']

def getResponse(q):
    q = q.replace('they', topic)
    q = q.replace('it', topic)
    sents.append(q)
    vectorizer = TfidfVectorizer()
    sents_vecs = vectorizer.fit_transform(sents)
    values = cosine_similarity(sents_vecs[-1], sents_vecs)
    response = sents[values.argsort()[0][-2]]
    sents.pop()
    return response.capitalize()

def learnMore():
  url = input("Can you teach me?")
  
  
  if ('http' in url):    
    data = urllib.request.urlopen(url).read()
    text = bsoup.BeautifulSoup(data, "html.parser").find_all('p')
    
    corpus = ''
    
    for t in text:
        corpus += t.text.lower()
    
    corpus_new = re.sub("[[].*[]]", "", corpus)
    
    text = nltk.sent_tokenize(corpus_new)
  
    for t in text:
      sents.append(t)
  else:
     sents.append(url)
  
q = ''
while (q != "bye"):
    q = input("What is your question?").lower()
    if (q != "bye"):  
        if ('not correct' in q or 'wrong' in q):
          learnMore()
        else:
          print(getResponse(q))  
    else:
        print("Goodbye!")
