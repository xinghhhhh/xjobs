import time

import jsyh.jobs.rootJob as rootJob

class weather(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    VERSION = "1.0"
    RELY = 'day.today_work.work1'
    def run(session, today_date):
        print( "weather begin!!!")
        print(today_date)
        time.sleep(5)
        print( "weather end!!!")


