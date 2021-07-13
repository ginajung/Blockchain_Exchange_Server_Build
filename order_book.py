from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Order
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# order ; dict object with 6 fields

def process_order(order):
    #Your code here
    # 1. set up new_order with 6 fields
    # 2. match with existing_order
    # 3. if matched, add order into table 
    
    pass