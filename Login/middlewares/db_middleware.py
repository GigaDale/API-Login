from controllers.db_controller import Db
from sqlalchemy import text

db = Db("mysql","pymysql", "root", "root", "localhost", 3306, "Contas")

def create_user(username, password):
    with db.connect() as conn:
        conn.execute(text(f"INSERT INTO login (username, password) VALUES ('{username}', '{password}')"))
        conn.commit()

def validation_login(username, password):
    with db.connect() as conn:       
        result = conn.execute(text(f"select * from login where username = '{username}' and password = '{password}'"))
        return len(result.all())