from redis import Redis
from rq_scheduler import Scheduler
from datetime import datetime

scheduler = Scheduler(connection=Redis())
def func(a,b,**kwargs):
     print a,b,kwargs
scheduler.cron(
    cron_string="*/1 * * * *",                # A cron string (e.g. "0 0 * * 0")
    func=func,                  # Function to be queued
    args=["a","c"],          # Arguments passed into function when executed
    kwargs={'foo': 'bar'},      # Keyword arguments passed into function when executed
    repeat=10                   # Repeat this number of times (None means repeat forever)

)
