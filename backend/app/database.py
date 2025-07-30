import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

# def get_db_conn():
#     dsn = oracledb.makedsn(
#         os.getenv("ORACLE_HOST", "localhost"),
#         int(os.getenv("ORACLE_PORT", 1521)),
#         service_name=os.getenv("ORACLE_SERVICE", "xe")
#     )
#     conn = oracledb.connect(
#         user=os.getenv("ORACLE_USER", "ynchoi"),
#         password=os.getenv("ORACLE_PASSWORD", "chldPsk"),
#         dsn=dsn
#     )
#     return conn

def get_db_conn():
    dsn = oracledb.makedsn(
        os.getenv("ORACLE_HOST", "localhost"),
        int(os.getenv("ORACLE_PORT", 1521)),
        service_name=os.getenv("ORACLE_SERVICE", "xe")
    )
    conn = oracledb.connect(
        user=os.getenv("ORACLE_USER", "mb"),
        password=os.getenv("ORACLE_PASSWORD", "mobridge"),
        dsn=dsn
    )
    return conn
