from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'

engine = create_engine(URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class TaskDB(Base):
    __tablename__ = 'task_elza'

    id = Column(Integer, primary_key=True)
    task_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    importance = Column(Integer, nullable=False)
    due_date = Column(DateTime, nullable=False)
