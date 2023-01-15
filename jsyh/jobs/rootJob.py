from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, DateTime
Base = declarative_base()


class xjobs(Base):
    __tablename__ = 'xjobs_jobinfo'

    JOB_NAME = Column(Text(100), primary_key=True)
    STATUS = Column(Text(10), default='')
    JOB_TYPE = Column(Text(10), default='')
    REPEAT_FLAG = Column(Text(1),default='')
    TODAY_FLAG = Column(Text(1), default='D')
    PRIORITY = Column(Integer, default=50)
    CREATE_TIME = Column(DateTime)
    START_TIME = Column(DateTime)
    END_TIME = Column(DateTime)
    RELY = Column(Text(1000), default='')
    VERSION = Column(Text(5), default='1.0')

    def run(self, today_date):
        print("================")
        pass


