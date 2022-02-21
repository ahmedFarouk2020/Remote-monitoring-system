import mysql.connector as DB

'''
host="Farouk21.mysql.pythonanywhere-services.com",
                user="Farouk21",
                password="database-sensor-esp-flask",
                database="Farouk21$sensors"
'''

class DB():
    def __init__(self, hostname, username, password, database_name) -> None:

        no_database = 0

        try :
            self.db = DB.connect(
                host=hostname,
                user=username,
                password=password,
                database=database_name
            )

        
        except:
            self.db = DB.connect(
                host=hostname,
                user=username,
                password=password
            )
            no_database = 1


        else:
            print("Error in creating DB!")
            exit(404)

        self.mycursor = self.db.cursor()

        if(no_database == 1):
            self.mycursor.execute(f"CREATE DATABASE {database_name}")

        self.mycursor.execute("CREATE TABLE readings (sensor1 VARCHAR(255), sensor2 VARCHAR(255))")

    def execute_sql_command(self,sql: str):
        """ execute sql commands which is in the form of formatted string """
        self.mycursor.execute(sql)
        self.db.commit()
