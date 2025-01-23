from sqlalchemy.sql import insert
from db_init import logs_table

def log_sign_in(engine, data):
    with engine.connect() as conn:
        stmt = insert(logs_table).values(data)
        conn.execute(stmt)
        conn.commit()