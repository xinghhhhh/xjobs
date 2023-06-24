#import mysql.connector
import configparser
from sqlalchemy import create_engine
#import pymysql
from sqlalchemy.orm import sessionmaker
import common.config.get_config as config
import ibm_db

HOST=config.get_config("mysql", "database_ip")
USER=config.get_config("mysql", "database_user")
PORT=config.get_config("mysql", "database_port")
PASSWD=config.get_config("mysql", "database_password")
DATABASE=config.get_config("mysql", "database_name")

# mydb = mysql.connector.connect(
#       host=HOST,
#       user=USER,
#       passwd=PASSWD,
#       database=DATABASE,
#       auth_plugin='mysql_native_password'
# )

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
    "db2+ibm_db://db2admin:db2admin@127.0.0.1:50000/test",
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

session = get_seesion()



# 连接字符串
# connStr = "DATABASE=TEST;HOSTNAME=127.0.0.1;PORT=50000;PROTOCOL=TCPIP;UID=db2admin;PWD=db2admin;"
# conn = None
# try:
#    # 连接数据库
#    conn = ibm_db.connect(connStr, "", "")
#    # 关闭自动提交
#    ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)
#    # 以插入语句为例,删除和更新只需要替换语句即可
#    sql = "insert into ods.table_1 values('%s', '%s')" % (2, "Jet")
#    # 执行SQL语句
#    stmt = ibm_db.exec_immediate(conn, sql)
#    # 获取受影响的行数
#    rows = ibm_db.num_rows(stmt)
#    # 提交事务
#    ibm_db.commit(conn)
# except Exception as ex:
#    # 回滚事务
#    ibm_db.rollback(conn)
# finally:
#    # 关闭数据库连接
#    ibm_db.close(conn)


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



