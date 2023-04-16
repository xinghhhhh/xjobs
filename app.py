from flask import Flask, render_template
import common.tools.db as db
import common.main.start as start
from concurrent.futures import ThreadPoolExecutor
import common.config.global_info as global_info
import time,datetime
import common.models.rootJob as models

session = db.get_seesion()
job_thread = ThreadPoolExecutor()
job_thread.submit(start.start)

def web_init():
    all_jobs = session.execute("SELECT job_name,repeat_flag,status,today_flag,count,rely,indirect_rely from xjobs_job").all()
    session.commit()
    tmp_dict = {}
    for job in all_jobs:
        tmp_dict[job[0]] = job[3]

    def get_flag(job_name):
        if tmp_dict[job_name] == 'Y':
            return 'Y'
        else:
            return 'N'

    web_json = {"nodes": [], "edges": []}
    for item in all_jobs:
        web_json["nodes"].append(
            {"id": item[0], "label": item[0], "repeat_flag": item[1], "status": item[2], "today_flag": item[3],
             "count": item[4]})
        if item[5] != '':
            rely_list = item[5].split(',')
            for source in rely_list:
                web_json["edges"].append({"source": source, "target": item[0], "source_flag": get_flag(source),
                                          "target_flag": get_flag(item[0]), "line_style": "direct"})
        if item[6] != '':
            indirect_rely_list = item[6].split(',')
            for source in indirect_rely_list:
                web_json["edges"].append({"source": source, "target": item[0], "source_flag": get_flag(source),
                                          "target_flag": get_flag(item[0]), "line_style": "indirect"})
    return web_json


app = Flask(__name__)



@app.route('/')
def hello_world():  #index
    init_josn = web_init()
    start.global_dict_init()
    return render_template("index.html", init_josn=init_josn, global_dict=global_info.global_dict)


@app.route('/stop_batch')
def stop_batch():
    if global_info.global_dict['batch_state'] != 'START':
        return 'N'
    else:
        batch_date = global_info.global_dict['batch_date']
        batch_date1 = datetime.strptime(batch_date, '%Y%m%d')
        session.query(models.batch_hst).filter(models.batch_hst.BATCH_DATE == batch_date1).update({"STATUS": 'PAUSE'})
        session.commit()
        result = global_info.modify_global_dict('batch_state', 'PAUSE')
        global_info.modify_global_dict('is_pause', 'Y')
        if result == 'Y':
            return 'Y'
        else:
            return 'N'


@app.route('/start_batch')
def start_batch():
    if global_info.global_dict['batch_state'] != 'PAUSE':
        return 'N'
    else:
        batch_date = global_info.global_dict['batch_date']
        batch_date1 = datetime.strptime(batch_date, '%Y%m%d')
        session.query(models.batch_hst).filter(models.batch_hst.BATCH_DATE == batch_date1).update({"STATUS": 'START'})
        session.commit()
        result = global_info.modify_global_dict('batch_state', 'START')
        if result == 'Y':
            return 'Y'
        else:
            return 'N'

@app.route('/change_batch_date')
def change_batch_date():
    start.change_batch_date('web')
    return 'Y'


@app.route('/run_jobs')
def run_jobs():
    start.run_batch()

    return 'Y'


if __name__ == '__main__':
    app.run()
