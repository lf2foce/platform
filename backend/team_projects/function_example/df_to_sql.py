import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///sqlite_dev.db', echo=True)  # see all of the output that comes from our database connection
sqlite_connection = engine.connect()

df = pd.DataFrame({'col1': ['test1', 'test2'], 'col2': [1,2]})

sqlite_table = "test_table"
df.to_sql(sqlite_table, sqlite_connection, if_exists='fail')

sqlite_connection.close()

# cmd
# sqlite3
# .open sqlite_dev.db
# sqlite> select * from test_table;