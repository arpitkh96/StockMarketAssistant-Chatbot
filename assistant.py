from __future__ import print_function
import json,config
import NLU
from watson_developer_cloud import AssistantV1

assistant = AssistantV1(
    username=config.assis_user,
    password=config.assis_pass,
    version='2017-04-21')
wid=config.wid
contexts={}
def message(text,channel):
    global contexts,assistant,wid
    context={'both':0}
    if channel in contexts:
        context=contexts[channel]
    response=assistant.message(wid,{ 'text':text},context=context)
    contexts[channel]=response['context']
    print(response,'\n')
    if response['intents'][0]['intent']=='onlyorg':
        possible_exchanges,companies=NLU.getCompany(text)
        if len(companies)>0:
            print('first if\n')
            context=response['context']
            context['org']=companies[0]['name']
            context['exch_count']=len(possible_exchanges)
            if(len(possible_exchanges)==1):
                context['exchange']=possible_exchanges[0]
            context['com']=1
            response=assistant.message(wid,{ 'text':"sissa#edoc"},context=context)
            contexts[channel]=response['context']
            print(response,'\n')
            return response['output']['text']  
        else:
            print('second if')
            context=response['context']
            context['org']=""
            context['com']=2
            print(context,'\n')
            response=assistant.message(wid,{ 'text':"sissa#edoc"},context=context)
            contexts[channel]=response['context']
            print(response,'\n')
            return response['output']['text']
    elif response['intents'][0]['intent']=='organdexchange':
        possible_exchanges,companies=NLU.getCompany(text)
        if len(companies)>0:
            print('first if\n')
            context=response['context']
            context['org']=companies[0]['name']
            if context['exchange'] is not None and context['exchange'] in possible_exchanges:
                context['exch_count']=1
            elif(len(possible_exchanges)==1):
                context['exch_count']=len(possible_exchanges)
                context['exchange']=possible_exchanges[0]
            elif (len(possible_exchanges)==2):
                context['exch_count']=len(possible_exchanges)

            context['com']=1
            response=assistant.message(wid,{ 'text':"sissa#edoc"},context=context)
            contexts[channel]=response['context']
            print(response,'\n')
            return response['output']['text']  
        else:
            print('second if')
            context=response['context']
            context['org']=""
            context['com']=2
            print(context,'\n')
            response=assistant.message(wid,{ 'text':"sissa#edoc"},context=context)
            contexts[channel]=response['context']
            print(response,'\n')
            return response['output']['text']
        
        
        return "Wait"
        
    return response['output']['text']
