from flask import Flask, render_template
import common.tools.db as db
import json

app = Flask(__name__)

session =db.get_seesion()
all_jobs = session.execute("SELECT job_name,repeat_flag,status,today_flag from xjobs_job")
today_jobs = session.execute("SELECT job_name,status from xjobs_job where today_flag='Y'")
all_jobs_rely = session.execute("SELECT job_name,rely from xjobs_job").all()
session.commit()
a_jobs=all_jobs.all()
t_jobs=today_jobs.all()


def covert_to_list(target):
    list = []
    for item in target:
        tem = []
        for i in item:
            tem.append(i)
        list.append(tem)
    return list


all_j = covert_to_list(a_jobs)
today_j = covert_to_list(t_jobs)


test_to_json = {"nodes":[],"edges":[]}
for job in all_j:
    test_to_json["nodes"].append({"id":job[0], "label": job[0], "shape": "rect", "status": job[2], "today_flag": job[3]})



for rely in all_jobs_rely:
    if rely[1] != '':
        tmp_list = rely[1].split(',')
        for rely_c in tmp_list:
            test_to_json["edges"].append({"source": rely_c, "target": rely[0]})
    else:
        continue
print(test_to_json)

@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html", all_jobs=all_j, today_jobs=today_j, graph_a=test_to_json)

@app.route('/tet')
def tet():
    return render_template("tet.html", graph_a=test_to_json)

if __name__ == '__main__':
    app.run()
