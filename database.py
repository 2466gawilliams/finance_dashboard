# database.py

from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# Define the base
Base = declarative_base()

# Define the FinancialEntry model
class FinancialEntry(Base):
    __tablename__ = 'financial_entries'
    
    id = Column(Integer, primary_key=True)
    user = Column(String, nullable=False)
    month = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    income = Column(Float, nullable=False)
    rent = Column(Float, nullable=False)
    utilities = Column(Float, nullable=False)
    groceries = Column(Float, nullable=False)
    transportation = Column(Float, nullable=False)
    entertainment = Column(Float, nullable=False)
    others = Column(Float, nullable=False)
    total_expenses = Column(Float, nullable=False)
    savings = Column(Float, nullable=False)
    timestamp = Column(Date, default=datetime.utcnow)

# Initialize the database
def init_db(db_path='finance.db'):
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Base.metadata.create_all(engine)
    return engine

# Get a session
def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
