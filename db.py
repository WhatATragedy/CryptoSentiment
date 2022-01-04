import psycopg2
import psycopg2.extras
from dataclasses import asdict
import json
from psycopg2 import sql
from typing import Dict, List


class DBUtil():
    def __init__(self):
        self.connection = psycopg2.connect(user = "postgres",
                                  password = "blah",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "postgres")
        self.cur = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    
    def create_table(self, table_name="crypto_sentiment", columns=[]):
        # self.cur.execute("DROP TABLE IF EXISTS crypto_sentiment;")
        self.connection.commit()
        self.cur.execute(f"""CREATE TABLE {table_name} (
                id SERIAL PRIMARY KEY,
                ticker TEXT,
                polarity decimal,
                subjectivity decimal,
                rank integer,
                date DATE
            );
        """)
        self.connection.commit()
    
    def upload_items_batch(self, sentiments: List[Dict] = list(dict())) -> bool:
        print([sentiment.__dict__ for sentiment in sentiments])
        try:
            self.cur.executemany("""
                INSERT INTO crypto_sentiment VALUES (
                    DEFAULT,
                    %(ticker)s,
                    %(polarity)s,
                    %(subjectivity)s,
                    %(rank)s,
                    %(date)s
                )
                ;
            """, [sentiment.__dict__ for sentiment in sentiments], )
            print(self.cur.execute)
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return True

    def does_item_exist(self, item):
        self.cur.execute(f"SELECT * FROM items WHERE boxId = %s;", (item.boxId,))
        result = self.cur.fetchone()
        return result
    
    def does_table_exist(self, table_name="crypto_sentiment"):
        self.cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", (table_name,))
        return self.cur.fetchone().get("exists")

    def does_table_have_items(self, table_name="crypto_sentiment"):
        self.cur.execute(
            sql.SQL("SELECT true FROM {} LIMIT 1")
        .format(sql.Identifier(table_name)))
        # This will return RealDictRow([('bool', True)]) or None depending on if there are items in the tale
        return self.cur.fetchone()






if __name__ == "__main__":
    db = DBUtil()
    db.create_table()