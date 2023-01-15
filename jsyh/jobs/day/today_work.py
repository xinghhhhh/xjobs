import static.rootJob as rootJob

class weather(rootJob.xjobs):
    job_name = __qualname__
    repeat_flag = "D"
    version = "1.0"
    def run(selft, today_date):
        print("今天不上班！！！")

