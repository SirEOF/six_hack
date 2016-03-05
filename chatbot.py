import os
import sys
import telepot
from telepot.delegate import per_chat_id, call, create_open
import logging
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

# Simulate a database to store unread messages
class DBStore(object):
    def __init__(self):
        self._db = {}

    def put(self, msg):
        chat_id = msg['chat']['id']

        if chat_id not in self._db:
            self._db[chat_id] = []

        self._db[chat_id].append(msg)

    # Pull all unread messages of a `chat_id`
    def pull(self, chat_id):
        messages = self._db[chat_id]
        del self._db[chat_id]

        # sort by date
        messages.sort(key=lambda m: m['date'])
        return messages

    # Tells how many unread messages per chat_id
    def unread_per_chat(self):
        return [(k,len(v)) for k,v in self._db.items()]


# Accept commands from owner. Give him unread messages.
class OwnerHandler(telepot.helper.ChatHandler):
    def __init__(self, seed_tuple, timeout, db):
        super(OwnerHandler, self).__init__(seed_tuple, timeout)
        self._db = db
        self._thread = {}

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(msg)
        if content_type != 'text':
            self.sender.sendMessage("I don't understand")
            return

        parser = Parser(msg['text'])
        parse = parser.parse_text(msg['text'].strip().lower())

        # in thread we store that we need to have for the conversation thread.

        if self._thread:
            action = self._thread['action']
        else:
            self._thread = {'action': parse['action'], 'json': parse}
            action = self._thread['action']


        # Tells who has sent you how many messages
        # end of thread set self._thread to None
        if action == 'transfer':
            self.sender.sendMessage('')
        # read next sender's messages
        elif action == 'block':
            pass
        elif action == 'add':
            pass
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


class ChatBox(telepot.DelegatorBot):
    def __init__(self, token):
        self._seen = set()
        self._store = DBStore()  # Imagine a dictionary for storing amounts.

        super(ChatBox, self).__init__(token, [
            # Here is a delegate to specially handle owner commands.
            (per_chat_id(), create_open(OwnerHandler, 20, self._store)),

            # For senders never seen before, send him a welcome message.
            (self._is_newcomer, custom_thread(call(self._send_welcome))),
        ])

    # seed-calculating function: use returned value to indicate whether to spawn a delegate
    def _is_newcomer(self, msg):
        chat_id = msg['chat']['id']

        if chat_id in self._seen:  # Sender has been seen before
            return None  # No delegate spawned

        self._seen.add(chat_id)
        return []  # non-hashable ==> delegates are independent, no seed association is made.

    def _send_welcome(self, seed_tuple):
        chat_id = seed_tuple[1]['chat']['id']

        print('Sending welcome ...')
        self.sendMessage(chat_id, 'Hello!')


if __name__ == '__main__':
    try:
        TOKEN = os.environ['TELEGRAM_TOKEN']
    except KeyError:
        logging.info('No telegram token')

    bot = ChatBox(TOKEN)
    bot.notifyOnMessage(run_forever=True)
