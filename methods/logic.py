from calendar import monthrange
from datetime import datetime, timedelta
from methods import db_methods, default_messages
import pytz

year_now = datetime.now().year
month_now = datetime.now().month
days_in_this_month = monthrange(year_now, month_now)[1]

data = {}

utc = pytz.utc
timezone = pytz.timezone('Asia/Singapore')

def check_format_message(message):
    shortcuts = ['tdy','today','tomorrow','tmr','tmrw']
    chat_id = message.chat.id
    chat_type = message.chat.type
    # keywords = ['set', '@']
    message = message.text
    message = message.split(' ')
    if len(message) < 3:
        return True
    if '@' not in message[1]:
        return 'No Time'
    if '/' not in message[2] and message[2] not in shortcuts:
        return 'No Date'
    if len(message) < 4: 
        return 'No Todo'
    if message[3] == 'repeat':
        return 'No Todo'
    
    # if chat_type == 'group' or chat_type == 'supergroup':
    #     if message.count('@') != 2:
    #         return True
    # if '-' in message:
    #     return True
    # if len(message.split(' ')) < 4:
    #     return 'No Todo'
    # if message.split(' ')[2] not in shortcuts and '/' not in message.split(' ')[2]:
    #     return 'No Date'

def process_message(message, date_to_check):
    chat_id = message.chat.id
    message = message.text
    message = message.lower()
    text_msg = message.split(' ')

    date_and_time, todo, repeat = extract_date_time_todo(text_msg)
    if type(date_and_time) == datetime  and (timezone.localize(date_and_time) < date_to_check):
        return default_messages.invalid_time_set
        # return str(timezone.localize(date_and_time)) + ' ' + str(date_time)
    if todo == 'valueError':
        return date_and_time
    if repeat == 'repeatError':
        return default_messages.invalid_repeat

    db_methods.insert_into_db(chat_id, date_and_time, todo, date_to_check, repeat)

    if repeat != None:
        return 'Your reminder: <b>"' + todo + '</b>"' + ' \nhas been set at ' + str(date_and_time) + '\nAnd will repeat (in): ' + repeat.upper()
 
    return 'Your reminder: <b>"' + todo + '</b>"' + ' \nhas been set at ' + str(date_and_time)

def find_correct_date_time(when_input,time):
    shortcuts ={
        'tmr' : 1,
        'tomorrow' : 1,
        'today' : 0,
        'tdy' : 0,
    }
    if when_input in shortcuts:
        set_date = datetime.now(timezone) + timedelta(shortcuts[when_input])
        month = str(set_date.date().month)
        if len(month) == 1:
            month = '0' + month
        set_date = str(set_date.date().day) + '/' + month + '/' + str(set_date.date().year)
    else:
        when_input = when_input.split('/')
        if len(when_input) < 3:
            when_input = when_input[0] + '/' + when_input[1] + '/2020'
        else:
            when_input = when_input[0] + '/' + when_input[1] + '/' + when_input[2]
        set_date = when_input
    correct_dt = set_date + ' ' + time
    try:
        datetime.strptime(correct_dt, "%d/%m/%Y %H:%M")
    except ValueError:
        return 'Invalid date, Please Try Again'
    return datetime.strptime(correct_dt, "%d/%m/%Y %H:%M")
    

def extract_date_time_todo(text_msg):
    repeat_key_words = ['weekly','daily', 'monthly', 'min', 'hour', 'everyday', 'mins']
    for block in text_msg[1:]:
        if '@' in block:
            time = str(block)
            break
    
    if len(time) < 5:
        return 'Invalid Time, Please Try Again', 'valueError'

    when = text_msg[text_msg.index(time) + 1]
    start_index_todo = text_msg.index(when) + 1
    todo = text_msg[start_index_todo:]
    repeat = None

    if 'repeat' in todo:
        index_of_repeat = todo.index('repeat')
        repeat = todo[index_of_repeat+1:]
        todo = todo[:index_of_repeat]

    time = time[1:3] + ':' + time[3:]
    if type(when) == str:
        when = when.lower()
    date_and_time = find_correct_date_time(when,time)
    if type(date_and_time) != datetime:
        return date_and_time, 'valueError' , repeat

    if repeat == []:
        return date_and_time, todo, 'repeatError'

    if repeat != None and len(repeat) > 1 :
        if repeat[-1] not in repeat_key_words:
            return date_and_time, todo, 'repeatError' 

    elif repeat != None:
        if 'min' not in repeat[-1] and 'hour' not in repeat[-1] and repeat[-1] not in repeat_key_words:
            return date_and_time, todo, 'repeatError'
    if repeat == None:
        return date_and_time, ' '.join(todo).upper(), repeat
    return date_and_time, ' '.join(todo).upper(), ''.join(repeat)


def retrieve_reminder_list(chat_id, date_to_check):
    db_methods.update_and_sort_db(chat_id, date_to_check)
    reminder_list = db_methods.retrieve_reminders_from_db(chat_id)
    if reminder_list != None:
        return 'You have the follow Reminders set: \n' + '\n'.join(reminder_list)
    return None

    
def remove_reminder(chat_id, idx, date_time):
    resp = db_methods.delete_reminder_from_db(chat_id, idx, date_time)
    if resp == True: 
        return 'Success'
    elif not resp:
        return 'Invalid'
    else:
        return resp