from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class FoodItem(Base):
    __tablename__ = 'food_items'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    expiry_date = Column(Date, nullable=True)
    owner = Column(String, nullable=True)
    location = Column(String, nullable=False)
    food_type = Column(String, nullable=False)
    other_tags = Column(String, nullable=True)

# Database setup
engine = create_engine('sqlite:///food_items.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
