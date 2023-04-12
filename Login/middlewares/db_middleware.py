from controllers.db_controller import Db
from sqlalchemy import text

db = Db("mysql","pymysql", "root", "root", "localhost", 3306, "Contas")

def create_login(usuario, senha):
    with db.connect() as conn:
        conn.execute(text(f"INSERT INTO login (usuario, senha) VALUES ('{usuario}', '{senha}')"))
        conn.commit()

def validation_login(usuario, senha):
    with db.connect() as conn:       
        result = conn.execute(text(f"select * from login where usuario = '{usuario}' and senha = '{senha}'"))
        return len(result.all())