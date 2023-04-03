from multiprocessing import freeze_support

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
jobs_path = config.get_config("common", "jobs_path").replace('\\', '.').replace('/', '.')

def insert_jobs():
    file_list = tools.scan_file(config.get_config("common", "project_path_win")+"\\"+config.get_config("common", "project_name")+"\\"+config.get_config("common", "path_name")+"\\jobs",None,".py")
    for file in file_list:
        module = tools.get_module_by_file(file)
        classes = tools.get_classes_by_module(module)
        for cls in classes:
            if cls.__bases__.__contains__(rootJob.xjobs):
                job_name = cls.__module__ .replace(jobs_path + '.', '') + "."+cls.__name__
                create_time = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime())
                today_flag = tools.get_today_flag(cls.REPEAT_FLAG)
                model_ = model.xjobs(JOB_NAME=job_name,
                                     STATUS=cls.STATUS,
                                     JOB_TYPE=cls.JOB_TYPE,
                                     REPEAT_FLAG=cls.REPEAT_FLAG,
                                     TODAY_FLAG=today_flag,
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

all_jobs = {}
def get_all_jobs():
    jobs = session.execute("SELECT job_name,status,priority,job_type,rely from xjobs_job where today_flag = 'Y' ")
    session.commit()
    for job in jobs.all():
        all_jobs[job[0]] = {'status': job[1], 'priority': job[2], 'job_type': job[3], 'rely': job[4]}



get_all_jobs()
def check_rely(job_name,rely):
    if len(rely) == 0:
        return 'Y'
    else:
        rely = rely.split(',')
        for item in rely:
            if all_jobs[item]['status'] != 'SUCCESS':
                return 'N'
            else:
                break
        return 'Y'

def get_ready_jobs(all):
    ready_jobs = []
    for item in all.keys():
        job_info = all[item]
        if (job_info['status'] == '' or job_info['status'] == 'FAILED') and check_rely(item, job_info['rely']) == 'Y':
            ready_jobs.append(item)
    return ready_jobs


@contextmanager
def job_context(job):
    #print("begin log ....")
    yield job
    #print("end log ....")


def run_job(target_job,batch_date):
    with job_context(target_job) as job:
        session = db.get_seesion()
        job_name = job.__module__+'.'+job.__name__
        tmp_dict = {'job_name': job_name[10:], 'status': ''} ##########################################
        start_time = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime())
        print(start_time)
        session.query(model.xjobs).filter(model.xjobs.JOB_NAME == job_name[10:]).update({"STATUS": "RUNNING", "START_TIME": start_time})
        session.commit()
        try:
            job.run(session, batch_date)
        except Exception as e:
            print(e)
            tmp_dict['status'] = 'FAILED'
            end_time = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime())
            session.query(model.xjobs).filter(model.xjobs.JOB_NAME == job_name[10:]).update({"STATUS": "FAILED", "END_TIME": end_time})
            session.commit()
        else:
            tmp_dict['status'] = 'SUCCESS'
            end_time = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime())
            session.query(model.xjobs).filter(model.xjobs.JOB_NAME == job_name[10:]).update({"STATUS": "SUCCESS", "END_TIME": end_time})
            session.commit()
        finally:
            pass
        return tmp_dict

def result_change(result):
    return main(result.result())


def put_job(num):
    ready=get_ready_jobs(all_jobs)
    if len(ready) != 0:
        for i in range(num):
            all_jobs[ready[i]]['status'] = 'RUNNING'
            job_class=tools.get_class_by_name(ready[i])
            thread_pool.submit(run_job, job_class, "20220403").add_done_callback(result_change)


def main(result):
    if len(result) == 0:
        put_job(2)
    else:
        print(result)
        job_name=result['job_name']
        job_result=result['status']
        all_jobs[job_name]['status'] = job_result
        put_job(1)

thread_pool = ThreadPoolExecutor(max_workers=2)

if __name__ == '__main__':
    freeze_support()
    begin={}
    main(begin)
    while True:
        print("pppppppppppppp")
        time.sleep(2)





