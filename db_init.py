import pymysql
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Date, Time, Boolean


metadata = MetaData()

logs_table = Table(
    "sign_in_logs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("date", Date, nullable=False),
    Column("time", Time, nullable=False),
    Column("firstName", String(100), nullable=False),
    Column("lastName", String(100), nullable=False),
    Column("userID", String(50)),
    Column("userType", String(50), nullable=False),
    Column("action", String(20), nullable=False),
    Column("grade", String(10)),
    Column("reason", String(255)),
    Column("returnTime", String(50)),
    Column("visitorPhone", String(20)),
    Column("visitorAffiliation", String(255)),
    Column("visitorLicensePlate", String(50)),
    Column("account", String(50)),
    Column("confirmed", Boolean, default=False),
)

def init_db(db_config):
    engine = create_engine(
        f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}",
        pool_recycle=1800,  # Recycle connections after 30 minutes
        pool_pre_ping=True
    )

    # Create tables if they do not exist
    metadata.create_all(engine)

    return engine
