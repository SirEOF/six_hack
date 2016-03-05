#!/usr/bin/env python
import json
import re


class Parser(object):

    def __init__(self, text):
        self.text = text

    def parse_text(self, text):
        # takes a string and returns returns functions with parameters
        print "\n\n\nYou texted:\n\n", text

        numbers = re.findall(r'\d+', text)
        phrase = text.split(' ') 
        currency = 'GBP'  
        acc_number = 0
        sort_code = 0
        amount = 0
        recepient = None

        # automatically assigning digit strings to needed fields
        for num in numbers:
            if len(num) == 6:
                sort_code = int(num)
            elif len(num) == 8:
                acc_number = int(num)
            else:
                amount = int(num)

        # finding the recepient's name in the phrase
        uppers = [x for x in phrase if x != phrase[0] and x[0].isupper()]
        if uppers: recepient = uppers[0]
        

        if any(x in phrase for x in ['block', 'lost', 'stole', 'stolen']):
            action = 'block'

        # transfer 20 to
        elif any(x in phrase for x in ['send', 'wire', 'transfer', 'owe']):   
            action = 'transfer'
            if 'to' in phrase:
                next = phrase[phrase.index('to') + 1]
                if not next.isdigit():
                    recepient = next
                else:
                    recepient = None

        elif any(x in phrase for x in ['add', 'alias', 'alias']):
            action = 'add'

        else:
            action = None    

        if not acc_number: acc_number = None
        if not sort_code: sort_code = None

        print json.dumps({"action": action,
                            "amount" : amount, 
                            "recepient" : {"name" : recepient, 
                                            "sort code" : sort_code, 
                                            "acc_number" : acc_number}, 
                            "currency" : currency})
    

msgs = [('send 20 to 23435465 812395'), ('send 150 to Bob'), ('I\'ve lost my card'),
        ('My card has been stolen'), ('let\'s block my card'), 
        ('add Bob\'s details: bank_acc: 12345678, sort 123456'), ('I owe Bob 20 quid')]

for x in msgs:
    y = Parser(x)
    y.parse_text(x)

