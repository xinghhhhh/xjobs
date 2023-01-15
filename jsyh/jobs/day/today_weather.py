import static.rootJob as rootJob

class weather(rootJob.xjobs):
    job_name = __qualname__
    repeat_flag = "D"
    version = "1.0"
    def run(self,yyy):
        print(yyy + "的天气是十分的美好！！！")

