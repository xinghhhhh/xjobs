import common.tools.db as db
import common.tools.init_tool as tools
import common.models.rootJob as model
from contextlib import contextmanager
import sqlalchemy
import time, threading, queue
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import multiprocessing
import common.config.get_config as config
import jsyh.jobs.rootJob as rootJob

session =db.get_seesion()

def insert_jobs():
    file_list = tools.scan_file(config.get_config("common", "project_path_win")+"\\"+config.get_config("common", "project_name")+"\\"+config.get_config("common", "path_name")+"\\jobs",None,".py")
    for file in file_list:
        module = tools.get_module_by_file(file)
        classes = tools.get_classes_by_module(module)
        for cls in classes:
            if cls.__bases__.__contains__(rootJob.xjobs):
                job_name = cls.__module__+"."+cls.__name__
                create_time = time.strftime("%Y-%m-%d %H-%M-%S",time.gmtime())
                today_flag = tools.get_today_flag(cls.REPEAT_FLAG)
                model_ = model.xjobs(JOB_NAME=job_name,
                                     STATUS = cls.STATUS,
                                     JOB_TYPE = cls.JOB_TYPE,
                                     REPEAT_FLAG = cls.REPEAT_FLAG,
                                     TODAY_FLAG = today_flag,
                                     COUNT = cls.COUNT,
                                     PRIORITY = cls.PRIORITY,
                                     CREATE_TIME = create_time,
                                     START_TIME = cls.START_TIME,
                                     END_TIME = cls.END_TIME,
                                     RELY = cls.RELY,
                                     VERSION = cls.VERSION
                                )
                session.add(model_)
    session.commit()

#插入任务
#insert_jobs()
def get_ready_jobs():
    jobs = session.execute("SELECT job_name,priority from xjobs_job where today_flag = 'Y' and status not in ('SUCCESS','RUNNING','ERROR') and GET_RELY_STATUS(rely) = 'Y' ORDER BY priority")
    session.commit()
    return jobs.all()

@contextmanager
def running_job(target_job,today_date):
    session = db.get_seesion()
    job_name = target_job.__module__+"."+target_job.__name__
    start_time = time.strftime("%Y-%m-%d %H-%M-%S",time.gmtime())
    session.query(model.xjobs).filter(model.xjobs.JOB_NAME == job_name).update({"STATUS":"RUNNING","START_TIME":start_time})
    session.commit()
    try:
        yield target_job.run(session, today_date)
    except Exception as e:
        print(e)
        end_time = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime())
        session.query(model.xjobs).filter(model.xjobs.JOB_NAME == job_name).update({"STATUS": "FAILED", "END_TIME": end_time})
        session.commit()
    else:
        end_time = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime())
        session.query(model.xjobs).filter(model.xjobs.JOB_NAME == job_name).update({"STATUS": "SUCCESS", "END_TIME": end_time})
        session.commit()
    finally:
        session.commit()
        session.close()

def run_job(target_job,today_date):
    with running_job(target_job, today_date) as job:
        pass

thread_pool = ThreadPoolExecutor(max_workers=2)

def mian():
    while True:
        print("========================")
        ready_jobs = get_ready_jobs()
        print(ready_jobs)
        for i in ready_jobs:
            job_class = tools.get_class_by_name(i[0])
            thread_pool.submit(run_job, job_class, "20230205")
        time.sleep(30)


