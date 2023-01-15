from db import mysqlw
from jsyh.jobs.rootJob import xjobs

session = mysqlw.get_seesion()
jobn = xjobs(JOB_NAME='tttt',
     STATUS='',
     JOB_TYPE='',
     REPEAT_FLAG='D',
     TODAY_FLAG='',
     PRIORITY=50,
     CREATE_TIME=None,
     START_TIME=None,
     END_TIME=None,
     RELY='',
     VERSION='1.0')

session.add(jobn)
session.commit()