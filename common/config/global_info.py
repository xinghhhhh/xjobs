import threading
#WAITING

global_dict = {"batch_state": "START", "batch_date": "19700101", "is_pause": "N", "running_num": "0"}
global_jobs_info = {}

lock = threading.RLock()


def get_all_jobs(all_jobs):
    global_jobs_info.clear()
    for job in all_jobs:
        global_jobs_info[job[0]] = {'status': job[1], 'priority': job[2], 'job_type': job[3], 'rely': job[4], 'indirect_rely': job[5], "run_stage": ""}


def modify_global_dict(key, value):
    lock.acquire()
    global_dict[key] = value
    lock.release()
    if global_dict[key] == value:
        return 'Y'
    else:
        return 'N'


def modify_jobs_info():
    global_jobs_info['day.today_work.work1']={}
    pass



def check_rely(rely,indirect_rely):
    if len(rely) == 0 and len(indirect_rely) == 0:
        return 'Y'
    elif len(rely) != 0 and len(indirect_rely) == 0:
        rely = rely.split(',')
        for item in rely:

            if item in global_jobs_info and global_jobs_info[item]['status'] != 'SUCCESS':
                return 'N'
            else:
                continue
        return 'Y'
    elif len(rely) == 0 and len(indirect_rely) != 0:
        indirect_rely = indirect_rely.split(',')
        for item in indirect_rely:
            if item in global_jobs_info and global_jobs_info[item]['status'] != 'SUCCESS':
                return 'N'
            else:
                continue
        return 'Y'
    else:
        rely1 = rely.split(',')
        rely2 = indirect_rely.split(',')
        rely1.extend(rely2)
        for item in rely1:
            if item in global_jobs_info and global_jobs_info[item]['status'] != 'SUCCESS':
                print("[[[[[[[[[[[[[[[[[[[[[[[[[[[")
                print(item)
                print("]]]]]]]]]]]]]]]]]]]]]]]]]")
                return 'N'
            else:
                continue
        return 'Y'


def thread_process(item):
    if global_jobs_info[item]['job_type'] == '':
        return 'Y'
    else:
        return 'N'

def get_ready_process_jobs():
    ready_process_jobs = []
    lock.acquire()
    for item in global_jobs_info.keys():
        job_info = global_jobs_info[item]
        if (job_info['status'] == '' or job_info['status'] == 'FAILED') and job_info['run_stage'] == '' and check_rely(job_info['rely'], job_info['indirect_rely']) == 'Y':
            if thread_process(item) == 'Y':
                ready_process_jobs.append(item)
                global_jobs_info[item]['run_stage'] = 'QUEUE'
    lock.release()
    return ready_process_jobs

def get_ready_thread_jobs():
    ready_thread_jobs = []
    lock.acquire()
    for item in global_jobs_info.keys():
        job_info = global_jobs_info[item]
        if (job_info['status'] == '' or job_info['status'] == 'FAILED') and job_info['run_stage'] == '' and check_rely(job_info['rely'], job_info['indirect_rely']) == 'Y':
            if thread_process(item) == 'N':
                ready_thread_jobs.append(item)
                global_jobs_info[item]['run_stage'] = 'QUEUE'
    lock.release()
    return ready_thread_jobs

def check_running_num():
    num = 0
    for item in global_jobs_info:
        if global_jobs_info[item]['status'] == 'RUNNING':
            num = num +1
    return num

def check_batch_status():
    num = 0
    for item in global_jobs_info:
        if global_jobs_info[item]['status'] != 'SUCCESS':
            num = num + 1
    return num