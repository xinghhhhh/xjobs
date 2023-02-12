from flask import Flask, render_template
import common.tools.db as db
import json

app = Flask(__name__)

session =db.get_seesion()
all_jobs = session.execute("SELECT job_name,repeat_flag from xjobs_job")
today_jobs = session.execute("SELECT job_name,status from xjobs_job where today_flag='Y'")
running_jobs = session.execute("SELECT job_name,status from xjobs_job where status='RUNNING'")
all_jobs_rely = session.execute("SELECT job_name,rely from xjobs_job").all()
session.commit()

a_jobs=all_jobs.all()
t_jobs=today_jobs.all()
r_jobs=running_jobs.all()

def covert_to_list(target):
    list = []
    for item in target:
        tem = []
        for i in item:
            tem.append(i)
        list.append(tem)
    return list


all_j = covert_to_list(a_jobs)
today_j = covert_to_list(today_jobs)
running_j = covert_to_list(running_jobs)

#all_j =[{name:value} for name,value in zip(key_list,value_list)]

graph_a={
            "nodes": [{
                    "id": 0,
                    "label": "流动人员",
                    "shape": "rect",
                    "name": "dddddddddddddddd"
                },
                {
                    "id": 1,
                    "label": "安全筛查",
                    "shape": "rect",
                    "name": "tttt"
                },
                {
                    "id": 2,
                    "label": "热像仪人体测温筛查",
                    "shape": "diamond",
                    "name": "ertw"
                },
                {
                    "id": 3,
                    "label": "人工复测",
                    "shape": "diamond",
                    "name":"hcfg"
                },
                {
                    "id": 4,
                    "label": "快速通过",
                    "shape": "rect",
                    "name": "rety"
                },
                {
                    "id": 5,
                    "label": "紧急处理",
                    "shape": "rect",
                    "name": "asda1"
                }
            ],
            "edges": [{
                    "source": 0,
                    "target": 1,
                    "label": ""
                },
                {
                    "source": 1,
                    "target": 2,
                    "label": ""
                },
                {
                    "source": 2,
                    "target": 4,
                    "label": "正常"
                },
                {
                    "source": 3,
                    "target": 5,
                    "label": "不正常"
                },
                {
                    "source": 3,
                    "target": 4,
                    "label": "什么鬼"
                },
                {
                    "source": 2,
                    "target": 3,
                    "label": "不正常"
                }
            ]
        }

test_to_json = {"nodes":[],"edges":[]}
import itertools
for job in all_j:
    test_to_json["nodes"].append({"id":job[0], "label": job[0], "shape": "rect"})


# for rely in all_jobs_rely:
#     if rely[1] != '':
#         print(rely[1])
#         tmp_list = rely[1].split(',')
#         for rely_c in tmp_list:
#             test_to_json["edges"].append({"source": rely[0], "target": rely_c})
#     else:
#         continue

for rely in all_jobs_rely:
    if rely[1] != '':
        print(rely[1])
        tmp_list = rely[1].split(',')
        for rely_c in tmp_list:
            test_to_json["edges"].append({"source": rely_c, "target": rely[0]})
    else:
        continue

print(test_to_json)

@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html", all_jobs=all_j, today_jobs=today_j, running_jobs=running_j)

@app.route('/tet')
def tet():
    return render_template("tet.html", graph_a=test_to_json)

if __name__ == '__main__':
    app.run()
