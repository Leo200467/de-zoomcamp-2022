from time import time

import pandas as pd
from sqlalchemy import create_engine


def ingest_data(user, pwd, host, port, db, table_name, csv_name):
    print(table_name, csv_name)

    engine = create_engine(f"postgresql://{user}:{pwd}@{host}:{port}/{db}")
    engine.connect()

    print('connected to database, starting insertion...')

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
