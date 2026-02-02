import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from airflow.hooks.postgres_hook import PostgresHook


class PostgresTripLoader:
    def __init__(self, postgres_conn_id: str, csv_path: str):
        self.postgres_conn_id = postgres_conn_id
        self.csv_path = csv_path
        self.df = None

        # self.conn_params = {
        #     "host": os.getenv("POSTGRES_HOST"),
        #     "port": int(os.getenv("POSTGRES_PORT", 5432)),
        #     "dbname": os.getenv("POSTGRES_DB"),
        #     "user": os.getenv("POSTGRES_USER"),
        #     "password": os.getenv("POSTGRES_PASSWORD"),
        # }

    def read_csv(self):
        self.df = pd.read_csv(
            self.csv_path,
            sep=";",
            quotechar='"',
            parse_dates=["trip_date"]
        )

    def convert_types(self):
        self.df["trip_id"] = self.df["trip_id"].astype(str)
        self.df["client_id"] = self.df["client_id"].astype(str)
        self.df["driver_id"] = self.df["driver_id"].astype(str)
        self.df["status"] = self.df["status"].astype(str)

    def insert_to_postgres(self):
        insert_sql = """
            INSERT INTO trips (trip_id, client_id, driver_id, trip_date, status)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (trip_id) DO NOTHING;
        """
        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        conn = hook.get_conn()
        cursor = conn.cursor()

        records = self.df[
            ["trip_id", "client_id", "driver_id", "trip_date", "status"]
        ].values.tolist()

        try:
            execute_batch(cursor, insert_sql, records, page_size=500)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Postgres insert failed: {e}")
        finally:
            cursor.close()
            conn.close()

    def run(self):
        self.read_csv()
        self.convert_types()
        self.insert_to_postgres()
