import argparse
import os
from time import time

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    pwd = params.pwd
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'output.csv'

    os.system(f"curl -kLSs {url} -o {csv_name}")

    engine = create_engine(f"postgresql://{user}:{pwd}@{host}:{port}/{db}")

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:

        t_start = time()

        df = next(df_iter)

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()

        print(f'inserted another chunk..., took {t_end - t_start} seconds')

parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

# user, password, host, port, database name, table name
# csv url

if __name__ == '__main__':

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--pwd', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table to write results')
    parser.add_argument('--url', help='url of the csv file')


    args = parser.parse_args()

    main(args)
