#!/usr/bin/env python
import json
import re


def parser(request):
    # takes a string and returns returns functions with parameters
    
    numbers = re.findall(r'\d+', request)
    phrase = request.split(' ') 
    currency = 'GBP'  

    for num in numbers:
        if len(num) == 6:
            sort_code = int(num)
        elif len(num) == 8:
            acc_number = int(num)
        else:
            amount = int(num)

    if all(x in phrase for x in ['card']):
        print request


    # transfer 20 to
    if any(x in phrase for x in ['send', 'wire', 'transfer']):   
        action = 'transfer'
        if 'to' in phrase:
            next = phrase[phrase.index('to') + 1]
            if not next.isdigit():
                recepient = next
            else:
                recepient = None
        

    if any(x in phrase for x in ['block', 'lost', 'stole', 'stolen']):
        action = 'block'


    return json.dumps({"action": action,
                        "amount" : amount, 
                        "recepient" : {"name" : recepient, 
                                        "sort code" : sort_code, 
                                        "acc_number" : acc_number}, 
                        "currency" : currency})
    

parser('send 20 to 23435465 812395')
parser('send 150 to Bob')
parser('I\'ve lost my card')
parser('My card has been stolen')
parser('let\'s block my card')
parser('add Bob\'s details: bank_acc: 12345678, sort 123456')

