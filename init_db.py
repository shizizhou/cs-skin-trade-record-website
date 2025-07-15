import csv
from database import Base, engine, SessionLocal
from model import Trade
import os

CSV_FILE = "cs.csv"

def init_database():
    print("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表已创建。")

def import_csv():
    if not os.path.exists(CSV_FILE):
        print(f"未找到文件 {CSV_FILE}，跳过导入。")
        return

    print(f"正在导入 CSV 数据：{CSV_FILE}")
    db = SessionLocal()

    with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                trade = Trade(
                    name=row["name"],
                    float_value=row["float"],
                    purchase_price=float(row["purchase price"]),
                    sell_price=float(row["sell price"]),
                    gross_income=float(row["gross income"]),
                    net_income=float(row["net income"]),
                    total_income=float(row["total income"])
                )
                db.add(trade)
            except Exception as e:
                print(f"导入失败：{row}，错误：{e}")

    db.commit()
    db.close()
    print("CSV 导入完成。")

if __name__ == "__main__":
    init_database()
    import_csv()