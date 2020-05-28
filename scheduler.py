from apscheduler.schedulers.blocking import BlockingScheduler
import helpers.find_jobs as find_jobs
from datetime import datetime
import pytz



sched = BlockingScheduler()


def run_get_jobs():
    timezone = pytz.timezone('Asia/Singapore')
    date_time_now = datetime.now(timezone)
    find_jobs.get_reminder_jobs(date_time_now)

run_time = datetime.now()
run_time = run_time.replace(minute=run_time.minute + 1, second=0)

print('starting now')
sched.add_job(func=run_get_jobs, trigger='interval', minutes=1, next_run_time=run_time)
sched.start()