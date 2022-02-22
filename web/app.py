from flask import Flask, render_template, request

from mysql_db import DB


db = DB("localhost", "farook", "database-sensor-esp-flask", "sensors")


app = Flask(__name__)


IDEL   = 0
ORDER1 = 1
ORDER2 = 2
server_order = IDEL

threshold1 = 50
threshold2 = 30

def report_decision(reading1, reading2):
    """ set <server_order> variable depending on sensor readings 

        EX: temperature is to high -> turn of the fan, esp!
    """

    global server_order
    if int(reading1) > int(threshold1):
        server_order = ORDER1

    if int(reading2) > int(threshold2):
        server_order = ORDER2




@app.route('/')
def route():
    return render_template("index.html")


@app.route('/get-server-order')
def read_sensors_data():
    """ return a value represent an order to esp depending on sensors data """
   
    return str(server_order)


@app.route('/get-sensor-data')
def store_sensors_data():
    """ store sensors readings in DB """


    s1 = request.args.get('s1')
    s2 = request.args.get('s2')

    sql = f"INSERT INTO readings (sensor1, sensor2) VALUES ({s1}, {s2})"
    db.execute_sql_command(sql)

    report_decision(s1,s2)

    return 'OK'

if __name__ == '__main__' :
    app.run(debug=True) # debug=True, host= '0.0.0.0', port=8090