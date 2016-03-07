# Pitch

Talk to your bank in human language through this [Telegram](https://telegram.org/) bot. You can tell it to send money, block your card and get a review of your spending habits. 

[![gif with examples](https://github.com/petr-tik/six_hack/blob/master/output.gif)](https://github.com/petr-tik/six_hack/blob/master/output.gif)

# Problems TeleBankBot solves:

## Card loss

### Traditional banks
- You've lost your card or someone stole it. 
- Need to look up the emergency number
- Call it, give your details
- Wait for them to confirm
- Call again to get a new card

### TeleBankBot

- Add your card with your own custom alias of the form my* and card number 

        Telegram_user, [06.03.16 11:09]
        Add myvisa/mymaestro/myworkcard 1234567890123456
        
        Sixhack_bank_bot, [06.03.16 11:09]
        Your card myvisa/mymaestro/myworkcard has been added. 
    
- Send it a short quick message in natual language to your bot and your current card is blocked and new one will be sent

    Telegram_user, [06.03.16 11:09]
    I've lost myvisa
    
    Sixhack_bank_bot, [06.03.16 11:09]
    Your card myvisa has been blocked. 
    Shall we order a new one?
    
    Telegram_user, [06.03.16 11:09]
    yes
    
    Sixhack_bank_bot, [06.03.16 11:19]
    New card is on the way


## Money Tranfer:

### Traditional banks
- log into online banking, find the person in the contacts book, choose amount, send. 

### TeleBankBot

- Create an alias for a person given their bank details 
- The alias will be saved in your bank's payment recipients

    Telegram_user, [06.03.16 12:27]
    add @friends_name (sort code) 123456 (acc_number) 12345678
    
    Sixhack_bank_bot, [06.03.16 12:27]
    We've succesfully added @friends_name to your list of recepients

- Drop it a normal message and reference your friend by alias

    Telegram_user, [06.03.16 12:28]
    I owe @friends_name 150 quid
    
    Sixhack_bank_bot, [06.03.16 12:28]
    Let's transfer some ca$h money to @friends_name
    
    Sixhack_bank_bot, [06.03.16 12:28]
    You have 5000 in your account and I'll send 150 to @friends_name.
    Please type digits 1, 5 and 6 of your password to confirm.
    
    Telegram_user, [06.03.16 12:28]
    1 4 3
    
    Sixhack_bank_bot, [06.03.16 12:28]
    Please confirm that you want to send 150 quid to @friends_name
    
    Telegram_user, [06.03.16 12:28]
    Yes
    
    Sixhack_bank_bot, [06.03.16 12:28]
    I just sent the money to @friends_name

- @friends_name receives a confirmation message (if their telegram name is their alias)

    Sixhack_bank_bot, [06.03.16 12:28]
    Hey @friends_name, @Telegram_user sent you 150 pounds. 
    Check your bank account and send your friend @Telegram_user a thank you message.


## Spending: 

### Traditional banks
- wait for a paper letter to come through the door or 
- log into your online bank to download a csv, which you need to parse in Excel


### TeleBankBot

- ask your bot what your spending has been like
- get a response and a recommendation, which category to watch


    Telegram_user, [06.03.16 11:08]
    What have I been spending on? 
    
    Sixhack_bank_bot, [06.03.16 11:08]
    You currently have 4725.0 pounds in your account and 
    here is the breakdown of your recent purchases by category
    You should watch your spending on entertainment
    
    Sixhack_bank_bot, [06.03.16 11:09]
![Photo](https://raw.githubusercontent.com/petr-tik/six_hack/master/spending_example.jpg)
    
