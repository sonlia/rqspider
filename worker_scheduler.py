#-*- coding:utf-8 -*-
#!/usr/bin/python
import sys
from rq_scheduler.scheduler import Scheduler

from rq_scheduler.utils import setup_loghandlers
from   settings.default_settings import DB_URL as url
from utils.database import db

def main(name):
    # pid = str(os.getpid())
    # with open("pid", 'w') as f:
    #     f.write(pid)
    d = db(url[name])
    setup_loghandlers("DEBUG")
    scheduler = Scheduler(connection=d, interval=2)

    scheduler.run(burst=False)
if __name__ == '__main__':
    sys.exit(main("run"))

