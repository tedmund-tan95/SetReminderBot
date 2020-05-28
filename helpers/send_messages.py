from app import send_reminder_to_user

def send_reminders_out(info):
    for job in info:
        send_reminder_to_user(job['chat_id'], job['todo'])

