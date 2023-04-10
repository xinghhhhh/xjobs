from flask import Flask, render_template
import common.tools.db as db
import json

app = Flask(__name__)

session =db.get_seesion()

def web_init():
    all_jobs = session.execute("SELECT job_name,repeat_flag,status,today_flag,count,rely from xjobs_job").all()
    session.commit()
    tmp_dict={}
    for job in all_jobs:
        tmp_dict[job[0]] = job[3]

    def get_flag(job_name):
        if tmp_dict[job_name] == 'Y':
            return 'Y'
        else:
            return 'N'
    web_json = {"nodes": [], "edges": []}
    for item in all_jobs:
        web_json["nodes"].append({"id": item[0], "label": item[0], "repeat_flag": item[1], "status": item[2], "today_flag": item[3], "count": item[4]})
        if item[5] != '':
            rely_list = item[5].split(',')
            for source in rely_list:
                web_json["edges"].append({"source": source, "target": item[0], "source_flag": get_flag(source), "target_flag": get_flag(item[0])})
    return web_json


@app.route('/')
def hello_world():  # put application's code here
    init_josn = web_init()
    return render_template("index.html", init_josn=init_josn)

@app.route('/tet')
def tet():
    return render_template("tet.html", graph_a=test_to_json)

if __name__ == '__main__':
    app.run()
