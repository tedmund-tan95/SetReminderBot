import pymongo
from pymongo import MongoClient
import ssl
import pytz, datetime
from methods import sensitive

timezone = pytz.timezone('Asia/Singapore')


def get_db():
    cluster = pymongo.MongoClient(sensitive.mongodb_token, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
    database = cluster.reminderbot
    db = database.jobs
    # database = cluster.testdatabase
    # db = database.testjobs
    return db

db = get_db()

def check_if_user_exist(chat_id):
    if db.find_one({'_id': chat_id}) != None:
        return True
    return False

def update_list_id(newlist):
    i = 1
    for reminder in newlist:
        reminder['list_id']  = i
        i += 1

def update_and_sort_db(chat_id, date_to_check):
    remove_older_ones(db, chat_id, date_to_check)
    find = db.find_one({'_id': chat_id})
    if find == None:
        return
    if find['data'] == []:
        db.delete_one({'_id':chat_id})
    else:
        new_sorted_list = sorted(find['data'], key=lambda k: k['date']) 
        update_list_id(new_sorted_list)
        new_count = len(new_sorted_list)
        db.update_one(
                    {'_id': chat_id},
                    {'$set': {'data' : new_sorted_list, 'data_count' : new_count }} 
                )

def remove_older_ones(db, chat_id, date_to_check):
    check = db.find_one({'_id': chat_id})
    if check != None:
        new_list = []
        for item in check['data']:
            if timezone.localize(item['date']) >= date_to_check:
                new_list.append(item)
        new_count = len(new_list)
        db.update_one(
                    {'_id': chat_id},
                    {'$set': {'data' : new_list , 'data_count' : new_count}} 
                )
                


def insert_into_db(chat_id, date, todo , date_to_check, repeat):
    if check_if_user_exist(chat_id):
        find = db.find_one({'_id': chat_id})
        find['data_count'] += 1
        to_update = {
            'list_id': find['data_count'],
            'date' : date,
            'todo' : todo,
            'repeat': repeat
        }
        find['data'].append(to_update)
        db.update_one(
            {'_id':chat_id},
            {'$set': {'data' : find['data'], 'data_count' : find['data_count'] }} 
        )
        update_and_sort_db(chat_id, date_to_check)
    else:
        to_add = {'_id': chat_id,
                'data_count' : 1,
                'data': [
                    {
                        'list_id': 1,
                        'date' : date,
                        'todo' : todo,
                        'repeat': repeat
                    }
                ]}
        db.insert_one(to_add)
    update_and_sort_db(chat_id, date_to_check)

def retrieve_reminders_from_db(chat_id):
    reminder_list = []
    if check_if_user_exist(chat_id):
        find = db.find_one({'_id': chat_id})
        for reminder in find['data']:
            if reminder['repeat'] != None:
                reminder_list.append(str(reminder['list_id']) + '. ' + "<b>" + reminder['todo'] + "</b>" + ' on ' + str(reminder['date']) + '\nrepeated(in): ' + str(reminder['repeat']).upper())
            else:
                reminder_list.append(str(reminder['list_id']) + '. ' + "<b>" + reminder['todo'] + "</b>" + ' on ' + str(reminder['date'] ))
        return reminder_list
    else:
        return None

def delete_reminder_from_db(chat_id, index, date_time):
    if check_if_user_exist(chat_id):
        find = db.find_one({'_id': chat_id})
        if index == 'all' : 
            db.delete_many({'_id' : chat_id})

            return 'all'
        else: 
            try :
                index = int(index)
            except 'ValueError':
                return 'Invalid index'
            finally:
                if any(d['list_id'] == index for d in find['data']):
                    db.update_one({'_id': chat_id}, {'$pull' : {'data' : {'list_id' : index}}})
                    update_and_sort_db(chat_id, date_time)
                    return True
                else:
                    return False
    return 'You do not have any Reminders set'


