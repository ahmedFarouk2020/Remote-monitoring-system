import mysql.connector as MySQL

'''
host="Farouk21.mysql.pythonanywhere-services.com",
                user="Farouk21",
                password="database-sensor-esp-flask",
                database="Farouk21$sensors"
'''
'''
                host="localhost",
                user="farook",
                password="database-sensor-esp-flask",
                database="sensors"
'''

class DB():
    def __init__(self, hostname, username, password, database_name) -> None:

        no_database = False

        try :
            self.db = MySQL.connect(
                host=hostname,
                user=username,
                password=password,
                database=database_name
            )
            print("try statement")

        except:
            self.db = MySQL.connect(
                host=hostname,
                user=username,
                password=password
            )
            print("except statement")


        self.mycursor = self.db.cursor(buffered=True)

        try:
            self.mycursor.execute(f"CREATE DATABASE {database_name}")
            self.mycursor.execute("CREATE TABLE readings (sensor1 VARCHAR(255), \
            sensor2 VARCHAR(255), id int(11) AUTO_INCREMENT )")

        except:
            pass


    def execute_sql_command(self,sql: str):
        """ execute sql commands which is in the form of formatted string """

        self.mycursor.execute(sql)
        try:
            self.db.commit()
        except:
            print("Changes already commited")



# db = DB("farook2022.mysql.pythonanywhere-services.com",
#             "farook2022",
#             "asd123#@!",
#             "farook2022$sensors")

# db = DB("localhost", "farook", "database-sensor-esp-flask", "sensors")

# readings = "readings"
# all = db.execute_sql_command(f"SELECT * FROM {readings}")
# print(all)