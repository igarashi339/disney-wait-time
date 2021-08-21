import datetime
import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor


class DBHandler:
    def __init__(self):
        load_dotenv()
        self.database_url = ""
        self.__init_database_url()

    def __init_database_url(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            self.database_url = str(os.environ['DATABASE_URL'])

    def update_raw_html(self, table_name, html_str):
        try:
            with psycopg2.connect(self.database_url, sslmode='require') as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    datetime_str = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))))
                    cur.execute("INSERT INTO " + table_name + " VALUES (\'"+ html_str +"\', \'" + datetime_str + "\');")
                conn.commit()
        except Exception as e:
            print(e.__str__())

    def get_single_record(self, table_name):
        with psycopg2.connect(self.database_url, sslmode='require') as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM " + table_name + " ORDER BY updated_time DESC")
                return cur.fetchone()
