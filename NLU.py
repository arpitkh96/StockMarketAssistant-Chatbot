import json,config
import requests
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions


natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2017-02-27',
    username=config.NLU_user,
    password=config.NLU_pass)

def getCompany(text):
    try:
        response = natural_language_understanding.analyze(text=text,features=Features(entities=EntitiesOptions()))
        if 'entities' in response:
            for entity in response['entities']:
                if entity['type']=='Company':
                    print(entity,'\n')
                    name=None
                    if 'disambiguation' in entity:
                        name= entity['disambiguation']['name']
                    else :
                        name= entity['text']
                    possible_exchanges,results,otherExchange= queryExchange(name)
                    return possible_exchanges,results,otherExchange
    except Exception as e:
        print("error "+e)
    return [],[],False        

def queryExchange(company):
    PARAMS = {'lang':'en','query':company}
 
# sending get request and saving the response as response object
    r = requests.get(url = 'http://d.yimg.com/autoc.finance.yahoo.com/autoc', params = PARAMS).json()
    possible_exchanges=[]
    results=[]
    otherExchange=True
    print(r['ResultSet']['Result'])
    for i in r['ResultSet']['Result']:
        if i['exch'] in ['NSI','BSE']:
            if len(results)==0:
                possible_exchanges.append(i['exch'])
                results.append(i)
            elif results[0]['name']==i['name']:
                possible_exchanges.append(i['exch'])
                results.append(i)
        # else:
        #     otherExchange=True
    return possible_exchanges,results,otherExchange
