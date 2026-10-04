import oracledb

oracledb.init_oracle_client(
    lib_dir=r"C:\oracle\instantclient_19_32"
)

def get_connection():
    connection = oracledb.connect(
        user="SCOTT",
        password="YOUR_ACTUAL_PASSWORD",
        dsn="localhost:1521/orcldee"
    )

    return connection