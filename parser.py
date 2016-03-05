#!/usr/bin/env python
import json
import re


class Parser(object):
    """
gets a text message and returns a json file (same format for everyone) with all relevant data fields


separate methods:
    get number details


    """
    def __init__(self, text):
        self.text = text
        self.numbers = re.findall(r'\d+', text)
        self.phrase = text.split(' ')
        self.currency = 'GBP'
        self.to_add = None # 'card' or 'person'
        self.amount = 0
        self.acc_number = None
        self.sort_code = None
        self.card_alias = None
        self.card_number = None
        self.action = None
        self.user_alias = None

    def get_number_details(self):
        for num in self.numbers:
            if len(num) == 6:
                self.sort_code = int(num)
            elif len(num) == 8:
                self.acc_number = int(num)
            elif len(num) == 16:
                self.card_number = int(num)
            else:
                self.amount = int(num)

    def get_user_alias(self):
        # finding user alias
        if 'to' in self.phrase:
                next = self.phrase[self.phrase.index('to') + 1]
                if not next.isdigit():
                    self.user_alias = next
                else:
                    self.user_alias = None

        else:
            # finding the recepient's name in the phrase by capital letter
            uppers = [x for x in self.phrase if x != self.phrase[0] and x[0].isupper()]
            if uppers:
                # make sure genetive Bob's/John's isn't included in the alias
                if "'" in uppers[0]:
                    idx = uppers[0].find("'")
                    self.user_alias = uppers[0][:idx]

    def get_card_alias(self):
        # finding card alias in phrase my____
        result = re.findall(r'my\w+', self.text)
        if result:
            self.card_alias = result[0]

    def choose_action(self):
        print "\n\n\nYou texted:\n\n", self.text

        # block card
        if any(x in self.phrase for x in ['block', 'lost', 'stole', 'stolen']):
            self.action = 'block'
            self.get_card_alias()

        # transfer money
        elif any(x in self.phrase for x in ['send', 'wire', 'transfer', 'owe']):
            self.action = 'transfer'
            self.get_user_alias()
            self.get_number_details()

        # adding new cards or friend's details
        elif any(x in self.phrase for x in ['add', 'alias']):
            self.action = 'add'
            self.get_number_details()
            self.get_user_alias()
            self.get_card_alias()
            if self.card_alias or self.card_number:
                self.to_add = 'card'
            elif self.user_alias or self.sort_code or self.acc_number:
                self.to_add = 'person'
                

        # statement action by words like 
        elif any(x in self.phrase for x in ['spent', 'spending', 'history', 'statement']):
            self.action = 'statement'

        else:
            self.get_number_details()
            self.action = None

    def parse_text(self):
        self.choose_action()
        dct = {"action": self.action,
                "to_add" : self.to_add,
                "amount" : self.amount,
                "recepient" : {
                                "user_alias": self.user_alias,
                                "sort_code": self.sort_code,
                                "acc_number": self.acc_number
                                },
                "card" : {
                                "card_alias": self.card_alias,
                                "card_number": self.card_number
                                },
                "currency" : self.currency}

        print json.dumps(dct)
        return dct


if __name__ == '__main__':
    msgs = ['send 20 to 23435465 812395', 'send 150 to Bob', 'I\'ve lost mymaestro',
        'mymaestro has been stolen', 'let\'s block mymaestro',
        'add Bob\'s details: bank_acc: 12345678, sort 123456', 'I owe Bob 20 quid', 
        'add new card: mymaestro, 1234567890123456', 'how have I been spending?', 
        'How much have I spent recently?', 'what\'s my banking history?']

    for x in msgs:
        y = Parser(x)
        y.parse_text()
