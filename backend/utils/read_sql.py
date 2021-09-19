import pickle
import pymysql

# mysqlclient
import pandas as pd
import pymysql.cursors
import ast
import json

# fob = open('my_student','wb') # file handling object is created
# pickle.dump(my_data,fob) # generated the Pickle
# fob.close()


# Connect to the database
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="oa_platform",
    charset="utf8mb4",
    # cursorclass=pymysql.cursors.DictCursor,
)

with connection:
    # with connection.cursor() as cursor:
    #     # Create a new record
    #     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    #     cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # # connection is not autocommit by default. So you must commit to save
    # # your changes.
    # connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `job_state` FROM `apscheduler_jobs` WHERE `id`=%s"
        cursor.execute(sql, ("project1.main_cv",))
        result = cursor.fetchone()
        # print(result)

    my_data = pd.read_sql("SELECT * FROM apscheduler_jobs LIMIT 5;", connection)

print(my_data)
print(type(my_data.loc[1, "job_state"]))
print(pickle.loads(my_data.loc[1, "job_state"]))
