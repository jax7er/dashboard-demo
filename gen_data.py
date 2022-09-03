import random
from datetime import datetime
from time import sleep

import psycopg2 as pg

conn_config = dict(
    host="tyke.db.elephantsql.com",
    database="esvuwiyz",
    user="esvuwiyz",
    password="Qg3nCkxxgp2fneMVZqUwEnSYuEGQiWlc",
)

with pg.connect(**conn_config) as conn, conn.cursor() as cur:
    while True:
        sql = (
            # f"CREATE TABLE IF NOT EXISTS test ({','.join(f'{c} {config.type}' for c, config in cols.items())});"
            f"INSERT INTO test (time, data) VALUES ('{datetime.now().isoformat(timespec='seconds')}',{random.randint(-2**31, 2**31 - 1)});"
        )

        print(sql)

        cur.execute(sql)
        conn.commit()

        sleep(1)
