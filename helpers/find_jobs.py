import pymongo, ssl, sys, pytz, string 
from pymongo import MongoClient
from datetime import datetime, timedelta
import methods.db_methods as db_methods
from helpers.send_messages import send_reminders_out

timezone = pytz.timezone('Asia/Singapore')

def get_all_jobs():
    db = db_methods.get_db()
    all_jobs = list(db.find({}))
    return all_jobs

def get_reminder_jobs(run_time):
    jobs_to_add = []
    reminder_jobs_to_execute = []
    all_jobs = get_all_jobs()
    for chat in all_jobs:
        chat_id = chat['_id']
        data = chat['data']
        for reminder in data:
            job = {}
            todo_date = reminder['date']
            idx = reminder['list_id']
            if todo_date.date() == run_time.date() and todo_date.hour == run_time.hour and todo_date.minute == run_time.minute:
                job = {
                    'chat_id': chat_id,
                    'todo' : reminder['todo'],
                    'date' : todo_date
                }
            if job != {}:
                if reminder['repeat'] != None:
                    jobs_to_add.append((chat_id,reminder))
                db_methods.delete_reminder_from_db(chat_id,idx, run_time)
                reminder_jobs_to_execute.append(job)
    if reminder_jobs_to_execute != []:
        send_reminders_out(reminder_jobs_to_execute)
    if jobs_to_add != []:
        for chat_id, reminder in jobs_to_add:
            repeated_reminder(chat_id,reminder)

def repeated_reminder(chart_id,reminder):
    reminder_keywords = {
        'weekly' : reminder['date'].replace(day=reminder['date'].day+7),
        'daily': reminder['date'].replace(day=reminder['date'].day+1),
        'monthly': reminder['date'].replace(month=reminder['date'].month+1), 
        'everyday': reminder['date'].replace(day=reminder['date'].day+1),
    }
    if reminder['repeat'] not in reminder_keywords:
        duration, time = extract_hour_min(reminder['repeat'])
        if time == 'min' or time == 'mins':
            reminder['date'] = reminder['date'] + timedelta(minutes=duration)
        elif time == 'hour':
            reminder['date'] = reminder['date'] + timedelta(hours=duration)
    else:
        reminder['date'] = reminder_keywords[reminder['repeat']]
    date_to_check = datetime.now(timezone)
    chat_id, date, todo ,repeat = chart_id, reminder['date'], reminder['todo'], reminder['repeat']
    db_methods.insert_into_db(chat_id, date, todo , date_to_check, repeat)

def extract_hour_min(repeat):
    for i in range(len(repeat)):
        if repeat[i] in string.ascii_lowercase:
            if repeat[:i] == '':
                duration = 1
            else:
                duration = int(repeat[:i])
            time = repeat[i:]
            return duration, time

