import time

import jsyh.jobs.rootJob as rootJob

class work1(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    VERSION = "1.0"

    def run(session, today_date):
        print("work1 开始")
        time.sleep(6)
        print("work1 结束")

class work2(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    RELY = 'day.today_work.work1'
    VERSION = "1.0"
    def run(session, today_date):
        print("work2 开始")
        time.sleep(5)
        print("work2 结束")

class work3(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    RELY = 'day.today_work.work2'
    VERSION = "1.0"
    def run(session, today_date):
        print("work3 开始")
        time.sleep(8)
        print("work3 结束")

class work4(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    RELY = 'day.today_work.work2'
    VERSION = "1.0"
    def run(session, today_date):
        print("work4 开始")
        time.sleep(8)
        print("work4 结束")

class work5(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    RELY = 'day.today_work.work2'
    VERSION = "1.0"
    def run(session, today_date):
        print("work5 开始")
        time.sleep(8)
        print("work5 结束")

class work6(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    RELY = 'day.today_weather.weather'
    VERSION = "1.0"
    def run(session, today_date):
        print("work6 开始")
        time.sleep(8)
        print("work6 结束")
class work7(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    RELY = 'day.today_work.work2'
    VERSION = "1.0"
    def run(session, today_date):
        print("work7 开始")
        time.sleep(8)
        print("work7 结束")
class work8(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    RELY = 'day.today_work.work2'
    VERSION = "1.0"
    def run(session, today_date):
        print("work8 开始")
        time.sleep(8)
        print("work8 结束")
class work9(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    RELY = 'day.today_work.work5,day.today_work.work6'
    VERSION = "1.0"
    def run(session, today_date):
        print("work9 开始")
        time.sleep(8)
        print("work9 结束")
class work10(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    RELY = 'day.today_work.work2'
    VERSION = "1.0"
    def run(session, today_date):
        print("work10 开始")
        time.sleep(8)
        print("work10 结束")
