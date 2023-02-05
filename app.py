from flask import Flask, render_template
import common.tools.db as db
import json

app = Flask(__name__)

session =db.get_seesion()
all_jobs = session.execute("SELECT job_name,repeat_flag from xjobs_job")
today_jobs = session.execute("SELECT job_name,status from xjobs_job where today_flag='Y'")
running_jobs = session.execute("SELECT job_name,status from xjobs_job where status='RUNNING'")
session.commit()

date=all_jobs.all()

key_list=[]
value_list=[]
for item in date:
    key_list.append(item[0])
    key_list.append(item[1])


#all_j =[{name:value} for name,value in zip(key_list,value_list)]
print(key_list)
len  = len(key_list)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html",all_j=key_list,len=len)


if __name__ == '__main__':
    app.run()
