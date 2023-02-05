import mysql.connector
import configparser
from sqlalchemy import create_engine
import pymysql
from sqlalchemy.orm import sessionmaker
import common.config.get_config as config

HOST=config.get_config("mysql", "database_ip")
USER=config.get_config("mysql", "database_user")
PORT=config.get_config("mysql", "database_port")
PASSWD=config.get_config("mysql", "database_password")
DATABASE=config.get_config("mysql", "database_name")

mydb = mysql.connector.connect(
      host=HOST,
      user=USER,
      passwd=PASSWD,
      database=DATABASE,
      auth_plugin='mysql_native_password'
)

class mysql():
   def query(sql):
      mycursor = mydb.cursor()
      mycursor.execute(sql)
      myresult = mycursor.fetchall()
      mydb.commit()
      mydb.close()
      return myresult

   def opt(sql):
      mycursor = mydb.cursor()
      result = mycursor.execute(sql)
      mydb.commit()
      mydb.close()
      return result


engine = create_engine(
    "mysql+pymysql://"+USER+":root@127.0.0.1:3306/xjobs",
    max_overflow=0,
    pool_size=5,
    pool_timeout=30,
    pool_recycle=-1
)


# conn = engine.raw_connection()
# cursor = conn.cursor()
# cursor.execute("select * from xjobs_jobinfo")
# rs = cursor.fetchall()

def get_seesion():
    DBsession = sessionmaker(bind=engine)
    seesion = DBsession()
    return seesion



#
# see = get_seesion()
# # DBsession = sessionmaker(bind=engine)
# # seesion = DBsession()
# jobn = xjobs(JOB_NAME='xxxx',
#      STATUS='',
#      JOB_TYPE='',
#      REPEAT_FLAG='D',
#      TODAY_FLAG='',
#      PRIORITY=50,
#      CREATE_TIME=None,
#      START_TIME=None,
#      END_TIME=None,
#      RELY='',
#      VERSION='1.0')
# # seesion.add(jobn)
# # seesion.commit()
#
# see.add(jobn)
# see.commit()


