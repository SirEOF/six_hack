#!/usr/bin/env python
import json
import re


def parser(request):
    # takes a string and returns returns functions with parameters
    
    numbers = re.findall(r'\d+', request)
    print numbers
    phrase = request.split(' ')
    
    for num in numbers:
        if len(num) == 6:
            sort_code = int(num)
        elif len(num) == 8:
            acc_number = int(num)
        else:

    if all(x in phrase for x in ['card']):
        print request


    # transfer 20 to
    if any(x in phrase for x in ['send', 'wire', 'transfer']):

        amount = 0
        currency = 'GBP'         
        if 'to' in phrase:
            recepient = phrase[phrase.index('to') + 1]
        else:
            #  telegram asks who to send to
            # 
            pass
    
    print json.dumps({"amount" : amount, 
                        "recepient" : {"name" : recepient, "sort code" : sort_code, "acc_number" : acc_number}, 
                        "currency" : currency})
    

parser('send 20 to 23435465 812395')
