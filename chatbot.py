import json
import logging
import re
import os
import sys

import requests
import telepot
from telepot.delegate import per_chat_id, create_open

from parser import Parser

"""
$ python3.2 chatbox_nodb.py <token> <owner_id>

Chatbox - a mailbox for chats

1. People send messages to your bot.
2. Your bot remembers the messages.
3. You read the messages later.

This version only stores the messages in memory. If the bot is killed, all messages are lost.
This version only handles text messages.

It accepts the following commands from you, the owner, only:

- /unread - tells you who has sent you messages and how many
- /next - read next sender's messages

It can be a starting point for customer-support type of bots.
"""

URL = 'http://14134b73.ngrok.io'


def check_json_complete(parsed, action):
    # takes action and json as received originally and returns a list of fields to complete
    # if list - empty, proceed to the next stage
    
    if action == 'block':
        # have to have either 
        if not parsed['card']['card_alias'] or not parsed['card']['card_number']:
            
    elif action == 'transfer':
        
    elif action == 'add':
        


    else:
        pass


# Simulate a database to store unread messages
class DBStore(object):
    def __init__(self):
        self._db = {}

    def get(self, msg, key):
        chat_id = msg['chat']['id']
        result = self._db.setdefault(chat_id, {}).get(key)
        return result

    def put(self, msg, key, value):
        chat_id = msg['chat']['id']
        self._db.setdefault(chat_id, {})[key] = value


# Accept commands from owner. Give him unread messages.
class OwnerHandler(telepot.helper.ChatHandler):
    def __init__(self, seed_tuple, timeout, db):
        super(OwnerHandler, self).__init__(seed_tuple, timeout)
        self._db = db
        self._thread = {}
        self_seen = set()

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(msg)
        if content_type != 'text':
            self.sender.sendMessage("I don't understand")
            return

        parser = Parser(msg['text'])
        parsed = parser.parse_text()

        # in thread we store that we need to have for the conversation thread.

        if self._thread:
            action = self._thread['action']
        else:
            self._thread = {'action': parsed['action'], 'json': parsed}
            action = self._thread['action']


        # Tells who has sent you how many messages
        # end of thread set self._thread to None
        if action == 'transfer':
            self.sender.sendMessage('Got it')
        # read next sender's messages
        elif action == 'block':

            dct = {
                'username': msg['from']['username'],
                'card_alias': parsed['card_alias'],
                'action': 'lock'
            }
            # r = requests.post(URL + '/card', data=json.dumps(dct))
        elif action == 'add':
            pass
            # r = requests.post(URL '/card',  )


        elif action = 'statement':
            
            #r = requests.post()

        elif action == 'cancel':
            self._thread = None

        else:
            # garbled message send custom keyboard
            # click one of the buttons, give example of what you can do
            self.sender.sendMessage("?")


import threading

class CustomThread(threading.Thread):
    def start(self):
        print('CustomThread starting ...')
        super(CustomThread, self).start()

# Note how this function wraps around the `call()` function below to implement
# a custom thread for delegation.
def custom_thread(func):
    def f(seed_tuple):
        target = func(seed_tuple)

        if type(target) is tuple:
            run, args, kwargs = target
            t = CustomThread(target=run, args=args, kwargs=kwargs)
        else:
            t = CustomThread(target=target)

        return t
    return f

class FirstTimeHandler(telepot.helper.ChatHandler):

    def __init__(self, seed_tuple, timeout, db, seen):
        super(FirstTimeHandler, self).__init__(seed_tuple, timeout)
        self._db = db
        self._seen = seen
        self._presented = False
        self.presented = False
        self.asked_secret = False
        self.asked_account = False

    def trigger_accountnumber(self, msg):
        if not self.asked_account:
            self.sender.sendMessage('What is your account number and sort code?')
            self.asked_account = True
        else:
            parser = Parser(msg['text'])
            parsed = parser.parse_text()
            self._db.put(msg, 'accountnumber', parsed['recepient']['acc_number'])
            self._db.put(msg, 'sortcode', parsed['recepient']['sort_code'])
            self.trigger_secretnumber(msg)

    def trigger_secretnumber(self, msg):
        if not self.asked_secret:
            self.sender.sendMessage('What is your secret bank code?')
            self.asked_secret = True
        else:
            m = re.search(r'\d+', msg['text'])
            if not m:
                self.asked_secret = False

            self._db.put(msg, 'secretnumber', m.group())
            self.sender.sendMessage('Thanks, I\'ll connect to the bank!')
            self.connect_to_bank(msg)

    def connect_to_bank(self, msg):
        data = {
            'username': msg['from']['username'],
            'accountnumber': self._db.get(msg, 'accountnumber'),
            'secretnumber': self._db.get(msg, 'secretnumber'),
            'sortcode': self._db.get(msg, 'sortcode')

        }
        r = requests.post(URL + '/start', data=json.dumps(data))
        print(r)


    def on_chat_message(self, msg):
        chat_id = msg['chat']['id']
        if not self.presented:
            self.sender.sendMessage('Welcome to Bankbot! ')
            self.sender.sendMessage('I need a few details first')
            self.presented = True

        if chat_id in self._seen:
            return None
        else:
            if not self._db.get(msg, 'accountnumber'):
                self.trigger_accountnumber(msg)
            elif not self._db.get(msg, 'secretnumber'):
                self.trigger_secretnumber(msg)


class ChatBox(telepot.DelegatorBot):
    def __init__(self, token):
        self._seen = set()
        self._store = DBStore()  # Imagine a dictionary for storing amounts.

        super(ChatBox, self).__init__(token, [
            # Here is a delegate to specially handle owner commands.
            # (per_chat_id(), create_open(OwnerHandler, 60*5, self._store)),
            (per_chat_id(), create_open(FirstTimeHandler, 60*5, self._store, self._seen))
            # For senders never seen before, send him a welcome message.
            # (self._is_newcomer, custom_thread(call(self._send_welcome))),
        ])

    # seed-calculating function: use returned value to indicate whether to spawn a delegate
    def _is_newcomer(self, msg):
        chat_id = msg['chat']['id']

        if chat_id in self._seen:  # Sender has been seen before
            return None  # No delegate spawned

        self._seen.add(chat_id)
        return []  # non-hashable ==> delegates are independent, no seed association is made.


if __name__ == '__main__':
    try:
        TOKEN = os.environ['TELEGRAM_TOKEN']
    except KeyError:
        logging.info('No telegram token')

    bot = ChatBox(TOKEN)
    bot.notifyOnMessage(run_forever=True)
