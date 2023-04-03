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
        print("work3 开始")
        time.sleep(8)
        print("work3 结束")

class work5(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    RELY = 'day.today_work.work2'
    VERSION = "1.0"
    def run(session, today_date):
        print("work3 开始")
        time.sleep(8)
        print("work3 结束")

class work6(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    RELY = 'day.today_work.work2'
    VERSION = "1.0"
    def run(session, today_date):
        print("work3 开始")
        time.sleep(8)
        print("work3 结束")
class work7(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    RELY = 'day.today_work.work2'
    VERSION = "1.0"
    def run(session, today_date):
        print("work3 开始")
        time.sleep(8)
        print("work3 结束")
class work8(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    RELY = 'day.today_work.work2'
    VERSION = "1.0"
    def run(session, today_date):
        print("work3 开始")
        time.sleep(8)
        print("work3 结束")
class work9(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    RELY = 'day.today_work.work2,day.today_work.work5'
    VERSION = "1.0"
    def run(session, today_date):
        print("work3 开始")
        time.sleep(8)
        print("work3 结束")
class work10(rootJob.xjobs):
    JOB_NAME = __qualname__
    REPEAT_FLAG = "D"
    RELY = 'day.today_work.work2'
    VERSION = "1.0"
    def run(session, today_date):
        print("work3 开始")
        time.sleep(8)
        print("work3 结束")
