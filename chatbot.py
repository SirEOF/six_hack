import json
import logging
import re
import os
import sys
import random

import requests
import telepot
from telepot.delegate import per_chat_id, create_open

from parser import Parser
from jokes import JOKES
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

URL = 'https://bhwbgbcbyj.localtunnel.me/'

USERS = {
    '@argparse': 98350863,
    '@druml': 201496951,
    '@thsc5000': 12498168,
    '@petr_tik': 157291539
}

def check_json_complete(parsed, action):
    # takes action and json as received originally and returns a list of fields to complete
    # if list - empty, proceed to the next stage

    if action == 'block':
        # have to have either
        if not parsed['card']['card_alias'] or not parsed['card']['card_number']:
            pass
    elif action == 'transfer':
        pass
    elif action == 'add':
        pass
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

    def insert_alias(self, msg):
        chat_id = msg['chat']['id']
        username = msg['from']['username']
        self._db.setdefault('usernames', {})[username] = chat_id

    def fetch_alias(self, username):
        alias_id = USERS.get(username)
        if not alias_id:
            raise KeyError('Alias not found')
        return alias_id


# Accept commands from owner. Give him unread messages.
class OwnerHandler(telepot.helper.ChatHandler):
    def __init__(self, seed_tuple, timeout, db, seen):
        super(OwnerHandler, self).__init__(seed_tuple, timeout)
        self._db = db
        self._seen = seen

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(msg)
        chat_id = msg['chat']['id']

        if chat_id not in self._seen:
            return

        if content_type != 'text':
            self.sender.sendMessage("I don't understand")
            return

        parser = Parser(msg['text'])
        parsed = parser.parse_text()
        action = parsed['action']

        if action == 'transfer':
            self.sender.sendMessage("Let's transfer some ca$h money")

        # read next sender's messages
        elif action == 'block':
            cardalias = parsed['card']['card_alias']
            dct = {
                'username': msg['from']['username'],
                'cardalias': cardalias,
                'action': 'block'
            }
            r = requests.post(URL + '/card', data=json.dumps(dct))
            if r.status_code == 200:
                self.sender.sendMessage("Your card {} has been blocked. \nShall we order a new one?".format(cardalias))

        elif action == 'add':
            if parsed['to_add'] == 'person':
                useralias = parsed['recepient']['user_alias']
                data = {
                    'username': msg['from']['username'],
                    'useralias': useralias,
                    'sortcode': parsed['recepient']['sort_code'],
                    'accountnumber': parsed['recepient']['acc_number']
                }
                r = requests.put(URL + '/alias', data=json.dumps(data))
                if r.status_code == 200:
                    self.sender.sendMessage(
                        "We've succesfully added {} to your list of recepients".format(useralias)
                    )
            elif parsed['to_add'] == 'card':
                cardalias = parsed['card']['card_alias']
                cardnumber = parsed['card']['card_number']
                data = {
                    'cardalias': cardalias,
                    'cardnumber': cardnumber,
                    'username': msg['from']['username']
                }
                r = requests.put(URL + '/card', data=json.dumps(data))
                if r.status_code == 200:
                    self.sender.sendMessage(
                        "Your card {} is now registered under alias: {}".format(cardnumber, cardalias)
                    )
            else:
                print('what do you want to add: card or friend?')

        elif action == 'statement':
            username = msg['from']['username']
            places = ['Starbucks', 'Waitrose', 'Tesco', 'Aldi']
            r = requests.get(URL + '/balance/{}'.format(username))
            if r.status_code == 200:
                self.sender.sendMessage("""You have {} pounds in your account.""".format(r.json()['balance'])),
                for _ in xrange(5):
                    num = float("{0:.2f}""".format(random.uniform(1.00, 30.00)))
                    self.sender.sendMessage("{}\t |\t {} |\t {}".format(num, 'outgoing', random.choice(places)))
        
        elif action == 'cancel':
            self._thread = None

        elif action == 'joke':
            self.sender.sendMessage(random.choice(JOKES))

        elif action == 'naughty':
            self.sender.sendMessage("Let's keep this professional, Sir")

        else:
            # garbled message send custom keyboard
            # click one of the buttons, give example of what you can do
            self.sender.sendMessage("What do you want me to do now?")


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
        self.sender.sendMessage('Now you can transfer money to your friends!')
        chat_id = msg['chat']['id']
        self._db.insert_alias(msg)
        self._seen.add(chat_id)

    def on_chat_message(self, msg):
        chat_id = msg['chat']['id']
        if not self.presented:
            self.sender.sendMessage('Welcome to Bankbot! ')
            self.sender.sendMessage('I need a few details first')
            self.presented = True

        if chat_id in self._seen:
            return None

        if not self._db.get(msg, 'accountnumber'):
            self.trigger_accountnumber(msg)
        elif not self._db.get(msg, 'secretnumber'):
            self.trigger_secretnumber(msg)

class TransferHandler(telepot.helper.ChatHandler):

    def __init__(self, seed_tuple, timeout, db, seen):
        super(TransferHandler, self).__init__(seed_tuple, timeout)
        self._db = db
        self._seen = seen
        self.recipient = None
        self.alias_id = None
        self.asked_password = None
        self.asked_confirmation = None
        self.current_thread = None
        # used by several, but not critical
        self.balance = None
        self.amount = None
        self.password = None

    def cancel(self):
        self.recipient = None
        self.alias_id = None
        self.asked_password = None
        self.asked_confirmation = None
        self.current_thread = None

    def trigger_password_question(self, msg, parsed):
        if not self.asked_password:
            username = msg['from']['username']
            r = requests.get(URL + '/balance/{}'.format(username))
            if r.status_code == 200:
                self.balance = format(r.json()['balance'])
            if self.amount > self.balance:
                self.sender.sendMessage('You can\'t send more than you have. Start over.')
                self.cancel()
                return
            message = """
            You have {} in your account and I'll send {} to {}. Please put in your password now.
            """.format(self.balance, self.amount, self.recipient)
            self.asked_password = True
            self.sender.sendMessage(message)
        else:
            m = re.search(r'\d+', msg['text'])
            self.password = m.group()
            print(self.password) # not needed for this demo.
            self.trigger_confirmation(msg)


    def trigger_confirmation(self, msg):
        if not self.asked_confirmation:
            message = """
                Please confirm that you want to send {}""".format(self.amount)
            self.sender.sendMessage(message, reply_markup={'keyboard': [['Yes','No']]})
            self.asked_confirmation = True
        else:
            # todo
            if msg['text'] == 'No':
                self.sender.sendMessage('All right, I won\'t send anything.')
                self.cancel()
            else:
                self.trigger_send_money(msg)

    def trigger_send_money(self, msg):
        # request to update money
        username = msg['from']['username']
        dct = {
        'from': username,
        'to': self.recipient,
        'amount': self.amount
        }
        r = requests.post(URL + '/transfer', data=json.dumps(dct))
        if r.status_code == 200:
            message = 'I sent the money to {}'.format(self.recipient)
            self.sender.sendMessage(message)
            m2 = 'Hey {}, {} sent you {}. Go on, send him a thank you message.'.format(self.recipient, username, self.amount)
            self.bot.sendMessage(USERS[self.recipient], m2)
            self.cancel()

    def on_chat_message(self, msg):
        # if chat_id not in self._seen:
        #     return
        print(msg)
        parser = Parser(msg['text'])
        parsed = parser.parse_text()

        # have another id to transfer and send a message.
        if self.current_thread:
            print("current thread, {}".format(self.current_thread))
        elif parsed['action'] != 'transfer':
            print('action isnt transfer')
            return
        elif parsed['action'] == 'transfer':
            print('action is transfer')
            self.current_thread = True
        if not self.recipient:
            print('no recipient')
            self.recipient = parsed['recepient']['user_alias']
            self.amount = int(parsed['amount'])
        try:
            self.alias_id = self._db.fetch_alias(self.recipient)
        except KeyError:
            self.sender.sendMessage('Oh oh, looks like your friend hasn\'t registered yet. Send him a message and let him know that he should register right away.')
            return

        print(self.current_thread)
        print(self.asked_password)

        if self.asked_confirmation:
            print('going to send money')
            self.trigger_confirmation(msg)
        elif self.asked_password:
            print('going to ask confirmation')
            self.trigger_confirmation(msg)
        elif self.recipient and self.alias_id:
            print('going to ask password')
            self.trigger_password_question(msg, parsed)

class ChatBox(telepot.DelegatorBot):
    def __init__(self, token):
        self._seen = set()
        self._store = DBStore()  # Imagine a dictionary for storing amounts.

        super(ChatBox, self).__init__(token, [
            # Here is a delegate to specially handle owner commands.
            (per_chat_id(), create_open(TransferHandler, 60*5, self._store, self._seen)),
            (per_chat_id(), create_open(OwnerHandler, 60*5, self._store, self._seen)),
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
