from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
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
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="trades")

    def to_dict(self):
        return {
            "name": self.name,
            "float_value": self.float_value,
            "purchase_price": self.purchase_price,
            "sell_price": self.sell_price,
            "gross_income": self.gross_income,
            "net_income": self.net_income,
        }


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    trades = relationship("Trade", back_populates="user")

