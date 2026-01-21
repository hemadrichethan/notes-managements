import mysql.connector as SQLC

# login to database
database_config = SQLC.connect(
    host = 'localhost',
    user = 'root', 
    password= 'root',
    database = "notes_management" # your mysql login password
)

# cursor object creation
cursor = database_config.cursor()
# print(database_config)
# print(cursor)

# create_database_query = "CREATE DATABASE IF NOT EXISTS APPLE;"
# # execute function is used to execute the sql queries
# cursor.execute(create_database_query)
# # selecting databse
# cursor.execute("USE APPLE;")
# fruits_table_query = """
#                     CREATE TABLE IF NOT EXISTS FRUITS(
#                     ID INT, 
#                     NAME VARCHAR(30),
#                     PRICE INT
#                 );"""
# cursor.execute(fruits_table_query)
# print('TABLE created successfully')
