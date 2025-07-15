from sqlalchemy import Column, Integer, String, Float
from database import Base

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    float_value = Column("float", String) 
    purchase_price = Column(Float)
    sell_price = Column(Float)
    gross_income = Column(Float)
    net_income = Column(Float)
    total_income = Column(Float)