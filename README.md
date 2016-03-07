# Pitch

Talk to your bank in human language through this [Telegram](https://telegram.org/) bot. You can tell it to send money, block your card and get a review of your spending habits. 

[![gif with examples](https://github.com/petr-tik/six_hack/blob/master/output.gif)](https://github.com/petr-tik/six_hack/blob/master/output.gif)

# Problems TeleBank solves:

Card loss
    Now
You've lost your card or someone stole it. Need to look up the emergency number, call it, give your details, which is tedious, costly and stops you from getting a new card. 

With TeleBank
quick message in natual language to your bot and your current card is blocked and new one will be sent

    Petr Tikilyaynen, [06.03.16 11:09]
    I've lost myvisa
    
    Sixhack_bank_bot, [06.03.16 11:09]
    Your card myvisa has been blocked. 
    Shall we order a new one?
    
    Petr Tikilyaynen, [06.03.16 11:09]
    yes
    
    Sixhack_bank_bot, [06.03.16 11:19]
    New card is on the way



Tranfer:
    Now
log into online banking, find the person in the contacts book, choose amount, send. 

    With TeleBank
ping a message with recipient's alias - money and notification is sent automatically

Create an alias for a person given their bank details 

    Petr Tikilyaynen, [06.03.16 12:27]
    add @friends_name (sort code) 123456 (acc_number) 12345678
    
    Sixhack_bank_bot, [06.03.16 12:27]
    We've succesfully added @friends_name to your list of recepients

Drop it a normal message and reference your friend by name

    Petr Tikilyaynen, [06.03.16 12:28]
    I owe @friends_name 150 quid
    
    Sixhack_bank_bot, [06.03.16 12:28]
    Let's transfer some ca$h money
    
    Sixhack_bank_bot, [06.03.16 12:28]
    You have 5000 in your account and I'll send 150 to @friends_name.
    Please type digits 1, 5 and 6 of your password to confirm.
    
    Petr Tikilyaynen, [06.03.16 12:28]
    1 4 3
    
    Sixhack_bank_bot, [06.03.16 12:28]
    Please confirm that you want to send 150 quid to @friends_name
    
    Petr Tikilyaynen, [06.03.16 12:28]
    Yes
    
    Sixhack_bank_bot, [06.03.16 12:28]
    I just sent the money to @friends_name

to @friends_name

    Sixhack_bank_bot, [06.03.16 12:28]
    Hey @friends_name, @me sent you 150 pounds. Check your bank account and send him a thank you message.




Spending: 
    Now
wait for a paper letter to come through the door
even with online banking apps you are given numbers you need to trawl

    With TeleBank
quick message
    get balance
    consumption distribution 
    in the last seven days you spent 

    Petr Tikilyaynen, [06.03.16 11:08]
    What have I been spending on? 
    
    Sixhack_bank_bot, [06.03.16 11:08]
    You currently have 4725.0 pounds in your account and here is the breakdown of your recent purchases by category
    
    Sixhack_bank_bot, [06.03.16 11:09]
    ![Photo](https://raw.githubusercontent.com/petr-tik/six_hack/master/spending_example.jpg)
    
    Sixhack_bank_bot, [06.03.16 11:09]
    You should watch your spending on entertainment




