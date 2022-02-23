from flask import Flask, render_template, request
from flask_pwa import PWA
from mysql_db import DB


#---------   Global Variables  -----
record_id = 0

IDEL   = 0
ORDER1 = 1
ORDER2 = 2
server_order = IDEL

threshold1 = 50
threshold2 = 30
#-----------------------------------

def create_app():
    app = Flask(__name__)
    PWA(app)

    @app.route('/')
    def home():
        return render_template("index.html")

    return app




db = DB("localhost", "farook", "database-sensor-esp-flask", "sensors")
# db = DB("farook2022.mysql.pythonanywhere-services.com",
#             "farook2022",
#             "asd123#@!",
#             "farook2022$sensors")
db.execute_sql_command('TRUNCATE TABLE readings')

def save_to_file():
    """ save a record to a file """


    sql = f"SELECT * FROM readings ORDER BY id DESC LIMIT 1"
    db.execute_sql_command(sql)

    
    sensor1_reading, sensor2_reading, record_id = db.mycursor.fetchone()
    print(sensor1_reading, sensor2_reading)
    with open('local-db/local.csv','a') as file:
        file.write(str(record_id)+','+str(sensor1_reading)+','+str(sensor2_reading)+'\r\n')
        file.close()


def report_decision(reading1, reading2):
    """ set <server_order> variable depending on sensor readings 

        EX: temperature is to high -> turn of the fan, esp!
    """

    global server_order
    if int(reading1) > int(threshold1):
        server_order = ORDER1

    if int(reading2) > int(threshold2):
        server_order = ORDER2



app = create_app()

# @app.route('/')
# def home():
#     return render_template("index.html")


@app.route('/get-server-order')
def read_sensors_data():
    """ return a value represent an order to esp depending on sensors data """
   
    return str(server_order)


@app.route('/get-sensor-data')
def store_sensors_data():
    """ store sensors readings in DB 
        Mobile app should only get the last line each time requesting this url
    """

    s1 = str(request.args.get('s1'))
    s2 = str(request.args.get('s2'))

    print(s1, s2)

    sql = f"INSERT INTO readings (sensor1, sensor2) VALUES ({s1}, {s2})"
    db.execute_sql_command(sql)

    report_decision(s1,s2)
    save_to_file()

    return 'OK'




@app.route('/retrieve-local-db')
def get_file_data():
    local_db = None
    with open('local.csv','r+') as file:
        local_db = file.read()
        file.truncate(0)
        file.close()

    return local_db
    

    
    

if __name__ == '__main__' :
    app.run(debug=True) # debug=True, host= '0.0.0.0', port=8090

