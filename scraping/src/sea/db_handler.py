import datetime
import os
import sys
import psycopg2
import json
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

    def exec_query(self, query_str):
        try:
            with psycopg2.connect(self.database_url, sslmode='require') as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    cur.execute(query_str)
        except Exception as e:
            print(e.__str__())

    def update_dynamic_data_table(self, table_name, data_str):
        """
        dynamic_dataテーブルを更新する。
        seaとlandの区別をつける必要が出てきた場合に備えて、テーブル名も指定できるようにしている。
        """
        datetime_str = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))))
        query_str = "INSERT INTO " + table_name + " VALUES (\'" + data_str + "\', \'" + datetime_str + "\');"
        self.exec_query(query_str)

    def select_resent_dynamic_data(self, table_name, date_num):
        """
        日数を指定して直近の動的情報を取得する。
        seaとlandの区別をつける必要が出てきた場合に備えて、テーブル名も指定できるようにしている。

        Return:
        ------
        date_str_list : array-like(obj)
            条件に合ったdataレコードの配列。
        """
        dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        dt_specified_time = dt_now - datetime.timedelta(days=date_num)
        query_str = "SELECT * from " + table_name +  " where datetime > \'" + str(dt_specified_time) + "\' order by datetime DESC"
        date_str_list = []
        try:
            with psycopg2.connect(self.database_url, sslmode='require') as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    cur.execute(query_str)
                    for row in cur:
                        date_str_list.append((row["datetime"], (json.loads(row["data"]))))
        except Exception as e:
            print(e.__str__())
            sys.exit()
        return date_str_list
