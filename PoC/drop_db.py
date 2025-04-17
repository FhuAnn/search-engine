from pymongo import MongoClient

def drop_db(db_name):
    # Kết nối tới MongoDB
    conn = "mongodb://localhost:27100,localhost:27200"
    client = MongoClient(conn)
    
    # Xóa cơ sở dữ liệu
    client.drop_database(db_name)
    print(f"Database '{db_name}' has been dropped.")

# Ví dụ sử dụng hàm drop_db
drop_db("search_engine")
