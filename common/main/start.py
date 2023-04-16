from multiprocessing import freeze_support
import common.tools.db as db
import common.tools.init_tool as tools
import common.models.rootJob as model
from contextlib import contextmanager
import sqlalchemy
import time, threading, queue
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future
import multiprocessing
import common.config.get_config as config
import jsyh.jobs.rootJob as rootJob
import schedule
import common.config.global_info as global_info

session = db.get_seesion()

thread_num = int(config.get_config("executor", "thread_pool_num"))
process_num = int(config.get_config("executor", "process_pool_num"))
jobs_path = config.get_config("common", "jobs_path").replace('\\', '.').replace('/', '.')

thread_pool = ThreadPoolExecutor(max_workers=thread_num)
process_pool = ProcessPoolExecutor(max_workers=process_num)


def insert_jobs():
    file_list = tools.scan_file(config.get_config("common", "project_path_win") + "\\" + config.get_config("common",
                                                                                                           "project_name") + "\\" + config.get_config(
        "common", "path_name") + "\\jobs", None, ".py")
    jobs_info = {}
    for file in file_list:
        module = tools.get_module_by_file(file)
        classes = tools.get_classes_by_module(module)
        for cls in classes:
            if cls.__bases__.__contains__(rootJob.xjobs):
                job_name = cls.__module__.replace(jobs_path + '.', '') + "." + cls.__name__
                create_time = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime())
                today_flag = tools.get_today_flag(cls.REPEAT_FLAG)
                jobs_info[job_name] = {"today_flag": today_flag, "rely": cls.RELY}
                model_ = model.xjobs(JOB_NAME=job_name,
                                     STATUS=cls.STATUS,
                                     JOB_TYPE=cls.JOB_TYPE,
                                     REPEAT_FLAG=cls.REPEAT_FLAG,
                                     TODAY_FLAG=today_flag,
                                     COUNT=cls.COUNT,
                                     PRIORITY=cls.PRIORITY,
                                     CREATE_TIME=create_time,
                                     START_TIME=cls.START_TIME,
                                     END_TIME=cls.END_TIME,
                                     RELY=cls.RELY,
                                     INDIRECT_RELY=cls.INDIRECT_RELY,
                                     VERSION=cls.VERSION
                                     )
                session.add(model_)
    session.commit()

    def check_indirect_rely(j_name):
        if jobs_info[j_name]['rely'].strip() != '':
            r_list = jobs_info[j_name]['rely'].split(',')
            for i in r_list:
                if jobs_info[i]['today_flag'] == 'Y':
                    tmp_indirect_rely.append(i)
                else:
                    check_indirect_rely(i)

    for key in jobs_info:
        if jobs_info[key]['today_flag'] == 'Y':
            tmp_indirect_rely = []
            if jobs_info[key]['rely'].strip() != '':
                rely_list = jobs_info[key]['rely'].split(',')
                for item in rely_list:
                    if jobs_info[item]['today_flag'] != 'Y':
                        check_indirect_rely(item)
            indirect_rely_str = ",".join(map(str, tmp_indirect_rely))
            session.query(model.xjobs).filter(model.xjobs.JOB_NAME == key).update({"INDIRECT_RELY": indirect_rely_str})
    session.commit()


# 插入任务
# insert_jobs()
# exit(0)

def jobs_init():
    jobs = session.execute("SELECT job_name,status,priority,job_type,rely,indirect_rely from xjobs_job where today_flag = 'Y' ")
    session.commit()
    global_info.get_all_jobs(jobs.all())


jobs_init()

@contextmanager
def job_context(job):
    # print("begin log ....")
    yield job
    # print("end log ....")


def run_job(target_job, batch_date, job_str_name):
    with job_context(target_job) as job:
        session = db.get_seesion()
        job_name = job.__module__ + '.' + job.__name__
        tmp_dict = {'job_name': job_str_name, 'status': ''}
        start_time = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime())
        print(start_time)
        session.query(model.xjobs).filter(model.xjobs.JOB_NAME == job_str_name).update({"STATUS": "RUNNING", "START_TIME": start_time})
        session.commit()
        try:
            job.run(session, batch_date)
        except Exception as e:
            print(e)
            tmp_dict['status'] = 'FAILED'
            end_time = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime())
            session.query(model.xjobs).filter(model.xjobs.JOB_NAME == job_str_name).update({"STATUS": "FAILED", "END_TIME": end_time})
        else:
            tmp_dict['status'] = 'SUCCESS'
            end_time = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime())
            session.query(model.xjobs).filter(model.xjobs.JOB_NAME == job_str_name).update({"STATUS": "SUCCESS", "END_TIME": end_time})
        finally:
            session.commit()
        return tmp_dict


def result_change(result):
    return main(result.result())


def put_job(thread_num, process_num):
    t_ready = global_info.get_ready_thread_jobs()
    p_ready = global_info.get_ready_process_jobs()
    batch_date = global_info.global_dict['batch_date']
    process_queue_num = process_pool._work_ids.qsize()
    thread_queue_num = thread_pool._work_queue.qsize()
    if len(t_ready) != 0:
        count = thread_num
        if len(t_ready) > thread_num:
            count = len(t_ready)
        for i in range(count):
            job_class = tools.get_class_by_name(t_ready[i])
            thread_pool.submit(run_job, job_class, batch_date, t_ready[i]).add_done_callback(result_change)
    if len(p_ready) != 0:
        count = process_num
        if len(p_ready) > process_num:
            count = len(p_ready)
        for i in range(count):
            job_class = tools.get_class_by_name(p_ready[i])
            process_pool.submit(run_job, job_class, batch_date, p_ready[i]).add_done_callback(result_change)



def main(result):
    if global_info.global_dict['batch_state'] == 'START':
        if len(result) == 0:
            put_job(5, 5)
        else:
            job_name = result['job_name']
            job_result = result['status']
            global_info.global_jobs_info[job_name]['status'] = job_result
            put_job(5, 5)
    else:
        pass

def check_status():
    if global_info.global_dict['is_pause'] == 'Y':
        num = global_info.check_running_num()
        if num == 0:
            time.sleep(3)
            num = global_info.check_running_num()
            if num == 0:
                global_info.modify_global_dict("is_pause", "N")
                global_info.modify_global_dict("batch_state", "STOP")
            else:
                pass
        else:
            pass
    else:
        num = global_info.check_batch_status()
        print("666666666666666666666666666")
        print(num)
        print("7777777777777777777")
        if num == 0:
            print("11111111111111111111111111")
            batch_date = global_info.global_dict['batch_date']
            print(batch_date)
            print("2222222222222222222222")
            batch_date1 = datetime.strptime(batch_date, '%Y%m%d')
            batch_date2 = datetime.strftime(batch_date1, '%Y-%m-%d')

            print(batch_date1)
            end_time = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime())
            print(end_time)
            session.query(model.batch_hst).filter(model.batch_hst.BATCH_DATE == batch_date2).update({"END_TIME": end_time, "STATUS": batch_date1})
            session.commit()
            global_info.modify_global_dict('batch_state', 'SUCCESS')
        print("888888888888888888888888888888888888")

def global_dict_init():
    latest_date = session.execute("SELECT BATCH_DATE,START_TIME,END_TIME,STATUS FROM XJOBS_BATCH_HST ORDER BY BATCH_DATE DESC LIMIT 1").all()
    print(latest_date)
    if latest_date[0][0] is None:
        today = datetime.date.today()
        model_ = model.batch_hst(
            BATCH_DATE=today,
            START_TIME=None,
            END_TIME=None,
            STATUS='NOT'
        )
        session.add(model_)
        session.commit()
    else:
        batch_date=latest_date[0][0].strftime('%Y%m%d')
        batch_state=latest_date[0][3]
        global_info.modify_global_dict('batch_date', batch_date)
        global_info.modify_global_dict('batch_state', batch_state)
        print(global_info.global_dict['batch_state'])




def change_batch_date(source):
    last_batch_date = global_info.global_dict['batch_date']
    last_batch_status = global_info.global_dict['batch_state']
    if source == 'web':
        if last_batch_status == 'SUCCESS':
            new_batch_date = datetime.strptime(last_batch_date, '%Y%m%d') + timedelta(days=1)
            model_ = model.batch_hst(
                BATCH_DATE=new_batch_date,
                START_TIME=None,
                END_TIME=None,
                STATUS='NOT'
            )
            session.add(model_)
            session.commit()
            global_dict_init()
    else:
        if last_batch_status == 'SUCCESS':
            new_batch_date = datetime.strptime(last_batch_date, '%Y%m%d') + timedelta(days=1)
            model_ = model.batch_hst(
                BATCH_DATE=new_batch_date,
                START_TIME=None,
                END_TIME=None,
                STATUS='NOT'
            )
            session.add(model_)
            session.commit()
            global_dict_init()
        else:
            print("昨天批量未结束！！")
            time.sleep(300)
            change_batch_date('start')


def run_batch():
    batch_date = global_info.global_dict['batch_date']
    batch_status = global_info.global_dict['batch_state']
    if batch_status == 'NOT':
        batch_date = global_info.global_dict['batch_date']
        batch_date1 = datetime.strptime(batch_date, '%Y%m%d')
        session.query(model.batch_hst).filter(model.batch_hst.BATCH_DATE == batch_date1).update({"STATUS": 'START'})
        session.commit()
        global_info.modify_global_dict('batch_state', 'START')
        print("=============================")
        begin = {}
        main(begin)
    else:
        print("不支持运行！")
        time.sleep(300)
        run_batch()


schedule.every(20).seconds.do(check_status)
schedule.every().day.at("00:00").do(change_batch_date)
schedule.every().day.at(config.get_config("batch", "begin_time"))

def start():
    while True:
        schedule.run_pending()

#start()
