import re
import json
import urllib2
from django.conf import settings
from xml.sax.saxutils import unescape

def nltk1(text):
    url = 'http://text-processing.com/api/sentiment/'
    data = 'text=' + text.encode('ascii', errors='backslashreplace')
    req = urllib2.Request(url, data, {'Content-Length': len(data)})
    response = urllib2.urlopen(req)
    js = response.readlines()
    js_object = json.loads(js[0])
    
    return js_object

def manish1(AnEmail):
    #MODULE 2: Take 'AnEmail' which is a text literal as input, and calculate its sentiment score

    # Sentiment analysis module
    # This module takes a string literal as input and returns a score value
    # Score = [1*(# positive words) - 1 (# negative words)]/total words

    positives = 0
    negatives = 0
    totalwords = 0
    score = 0
    negativewordlist = []
    positivewordlist = []
    processedwordlist = []
    AllWords = re.split('[ ,.\n\t\s\'-]', AnEmail)

    for nextword in AllWords:
        if len(nextword) >= 2:
            totalwords += 1
            processedwordlist.append(nextword)
            if nextword in settings.WORDDICT.keys():
                if settings.WORDDICT[nextword] == 'positive':
                    positivewordlist.append(nextword)
                    positives += 1
                elif settings.WORDDICT[nextword] == 'negative':
                    negativewordlist.append(nextword)
                    negatives += 1
    
    if totalwords != 0:
        score = (positives - negatives)/float(totalwords)

    response = {}
    response['debug'] = {}
    response['debug']['count'] = {}
    response['debug']['count']['positive'] = positives
    response['debug']['count']['negative'] = negatives
    response['debug']['count']['total'] = totalwords
    response['debug']['words'] = {}
    response['debug']['words']['positive'] = positivewordlist
    response['debug']['words']['negative'] = negativewordlist
    response['debug']['words']['all'] = processedwordlist
    response['score'] = score

    return response

def analyze(text):
    varmanish1 = manish1(text)
    varnltk1 = nltk1(text)

    response = {}
    response['detail'] = {}
    response['detail']['manish1'] = varmanish1
    response['detail']['nltk1'] = varnltk1

    neg = varnltk1['probability']['neg']
    pos = varnltk1['probability']['pos']
    neu = varnltk1['probability']['neutral']

    response['score'] = (pos - neg) / float(pos + neg) *  (1 - neu)
    response['objects'] = {}
    response['objects']['slider'] = getresult(response['score'])[1]
    response['objects']['number'] = getnumber(response['score'])
    response['objects']['text'] = getresult(response['score'])[0]

    response['text'] = text

    response['raw'] = unescape(json.dumps(response))

    return response

def getresult(score):
    small = 0.1
    medium = 0.2
    large = 0.3

    if score <= -large:
        return ['Angry', '1']
    elif score <= -medium and score > -large:
        return ['Negative', '2']
    elif score <= -small and score > -medium:
        return ['Somewhat negative', '3']
    elif score < small and score > -small:
        return ['Neutral', '4']
    elif score >= small and score < medium:
        return ['Somewhat positive', '5']
    elif score >= medium and score < large:
        return ['Positive', '6']
    elif score >= large:
        return ['Ecstatic', '7']

def getnumber(score):
    max = 0.3
    min = -max
    range = max - min
    interval = range / 8
    points = 0
    while points * interval < score + max and points < 9:
        points += 1

    return points + 1