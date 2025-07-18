import csv
from database import Base, engine, SessionLocal
from model import Trade
import os

CSV_FILE = "cs.csv"

def init_database():
    print("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表已创建。")


