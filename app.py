from flask import Flask, request
import telebot, pytz
from methods import logic, default_messages
from datetime import datetime
from methods.sensitive import actual_telegram_token, test_telegram_token, test_ngrok


# TOKEN = test_telegram_token #testerbot
TOKEN = actual_telegram_token #actualbot

bot = telebot.TeleBot(TOKEN)
URL = "https://telegram-bot-setreminderbot.herokuapp.com/"
# NGROK_URL = test_ngrok

utc = pytz.utc
timezone = pytz.timezone('Asia/Singapore')

# start the flask app
app = Flask(__name__)

def send_reminder_to_user(chat_id, todo):
    bot.send_message(chat_id, 'You have a reminder! : \n' + '<b>' + todo + '</b>',parse_mode='html')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.reply_to(message, default_messages.start_msg_all , parse_mode='html')
    welcome = default_messages.private_start
    if message.chat.type == 'group' or message.chat.type == 'supergroup' :
        welcome = default_messages.group_start
    bot.send_message(chat_id, welcome , parse_mode='MarkdownV2')

@bot.message_handler(commands=['help'])
def send_welcome(message):
    chat_id = message.chat.id
    welcome = default_messages.private_start
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        welcome = default_messages.group_start
    bot.reply_to(message, welcome , parse_mode='MarkdownV2')

@bot.message_handler(commands=['view'])
def send_reminder_list(message):
    chat_id = message.chat.id
    chat_type = message.chat.type

    set_error = default_messages.private_set_error
    no_reminder = default_messages.no_reminders

    if chat_type == 'group' or chat_type == 'supergroup':
        set_error = default_messages.group_set_error

    date_to_check = datetime.now(timezone)
    reminders = logic.retrieve_reminder_list(chat_id, date_to_check)
    if reminders == None:
        bot.reply_to(message, no_reminder)
        bot.send_message(chat_id, set_error , parse_mode='MarkdownV2')

    else:
        bot.send_message(chat_id, reminders , parse_mode='html')

@bot.message_handler(commands=['set', 'set@SetReminderBot', 'set@tedstester_bot '])
def set_reminder(message):
    chat_id = message.chat.id
    chat_type = message.chat.type
    date_to_check = datetime.now(timezone)

    set_error = default_messages.private_set_error
    empty_reminder = default_messages.empty_reminder
    empty_date = default_messages.empty_date
    empty_time = default_messages.wrong_format_time

    if chat_type == 'group' or chat_type == 'supergroup':
        set_error = default_messages.group_set_error
        empty_reminder = default_messages.empty_reminder_group
        empty_date = default_messages.empty_date_group
        empty_time = default_messages.wrong_format_time_group

    if logic.check_format_message(message) == True:
        bot.reply_to(message, set_error, parse_mode='MarkdownV2')
    elif logic.check_format_message(message) == 'No Todo':
        bot.reply_to(message, empty_reminder)
    elif logic.check_format_message(message) == 'No Date':
        bot.reply_to(message, empty_date)
    elif logic.check_format_message(message) == 'No Time':
        bot.reply_to(message, empty_time)
    else:
        reply = logic.process_message(message, date_to_check )
        bot.send_message(chat_id, reply, parse_mode='html')

@bot.message_handler(commands=['remove', 'remove@SetReminderBot', 'remove@tedstester_bot'])
def remove_reminder(message):
    chat_id = message.chat.id
    chat_type = message.chat.type
    date_time = datetime.now(timezone)

    user_input = message.text.split(' ')
    if logic.retrieve_reminder_list(chat_id, date_time) == None:
        bot.send_message(chat_id, default_messages.no_reminders)    
    elif len(user_input) == 1:
        bot.reply_to(message, default_messages.reminders_start)
        reminders = logic.retrieve_reminder_list(chat_id, date_time)
        bot.send_message(chat_id, reminders, parse_mode='html')
    else:
        idx = message.text.split(' ')
        resp = logic.remove_reminder(chat_id, idx[-1], date_time)
        if resp == 'Invalid': 
            bot.send_message(chat_id, 'Invalid Index, Please try again')
        elif resp == 'Success':
            bot.send_message(chat_id, 'Successfully removed reminder')
            # reminders = logic.retrieve_reminder_list(chat_id, date_time)
            # if reminders == None:
            #     bot.send_message(chat_id, default_messages.no_reminders)
            # else:
            #     bot.send_message(chat_id, reminders, parse_mode='html')
        elif resp == 'all':
            bot.send_message(chat_id, 'Successfully removed all reminders')
        else:
            bot.send_message(chat_id, 'Invalid Index, Please try again')


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    import time
    bot.remove_webhook()
    bot.set_webhook(url=URL + TOKEN)
    return "Set Webhook at " + URL+TOKEN, 200
    # bot.set_webhook(url=NGROK_URL+TOKEN)
    # return "Set Webhook at " + NGROK_URL, 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
