import sqlite3
import os

SQL_FILE = os.path.join(os.path.dirname(__file__), '../benkai_system.sql')
DB_FILE = os.path.join(os.path.dirname(__file__), 'benkai.db')

def init_db():
    with open(SQL_FILE, 'r', encoding='utf-8') as f:
        sql = f.read()
    conn = sqlite3.connect(DB_FILE)
    conn.executescript(sql)
    conn.close()
    print('数据库初始化完成')

if __name__ == '__main__':
    init_db() 