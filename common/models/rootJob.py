from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,DateTime

Base = declarative_base()

class xjobs(Base):
    __tablename__ = 'xjobs_job'
    #__table_args__ = {'schema':'ODS'}

    JOB_NAME = Column(String(100),primary_key=True)
    STATUS = Column(String(10),default='')
    JOB_TYPE = Column(String(10),default='')
    REPEAT_FLAG = Column(String(1),default='D')
    TODAY_FLAG = Column(String(1),default='')
    COUNT = Column(Integer,default=0)
    PRIORITY = Column(Integer,default=50)
    CREATE_TIME = Column(DateTime)
    START_TIME = Column(DateTime)
    END_TIME = Column(DateTime)
    RELY = Column(String(1000),default='')
    VERSION = Column(String(5),default='')

#初始化表
#import common.tools.db as db
#Base.metadata.create_all(db.engine)