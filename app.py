from flask import Flask, render_template
import common.tools.db as db
import json

app = Flask(__name__)

session =db.get_seesion()
all_jobs = session.execute("SELECT job_name,repeat_flag from xjobs_job")
today_jobs = session.execute("SELECT job_name,status from xjobs_job where today_flag='Y'")
running_jobs = session.execute("SELECT job_name,status from xjobs_job where status='RUNNING'")
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
print(all_j)



@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html", all_jobs=all_j, today_jobs=today_j, running_jobs=running_j)


if __name__ == '__main__':
    app.run()
