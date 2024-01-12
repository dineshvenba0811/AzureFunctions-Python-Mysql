import azure.functions as func
import datetime
import json
import logging
from azure.functions.decorators.core import DataType
import uuid
import mysql.connector
from mysql.connector import errorcode

app = func.FunctionApp()

@app.route(route="hello", auth_level=func.AuthLevel.ANONYMOUS)
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Create a connection pool
    config = {
    'host':'organisationwebapi-mysql.mysql.database.azure.com',
    'user':'sqladmin',
    'password':'Admin@123',
    'database':'dbo'
    }
    
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        try:
            conn = mysql.connector.connect(**config)
            print("Connection established")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cursor = conn.cursor()

        #insertDataIntotable(cursor)
        #readDataFromDatabase(cursor)
        #updateData(cursor)
        deleteData(cursor)
         # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
        print("Done.")

        return func.HttpResponse(f"Hello !")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

def insertDataIntotable(cursor):
    # Create table
    cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
    print("Finished creating table.")

    # Insert some data into table
    cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("banana", 150))
    print("Inserted",cursor.rowcount,"row(s) of data.")
    cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("orange", 154))
    print("Inserted",cursor.rowcount,"row(s) of data.")
    cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("apple", 100))
    print("Inserted",cursor.rowcount,"row(s) of data.")

def readDataFromDatabase(cursor):
    cursor.execute("SELECT * FROM inventory;")
    rows = cursor.fetchall()
    print("Read",cursor.rowcount,"row(s) of data.")
    # Print all rows
    for row in rows:
  	    print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))

def updateData(cursor):
    cursor.execute("UPDATE inventory SET quantity = %s WHERE name = %s;", (200, "banana"))
    print("Updated",cursor.rowcount,"row(s) of data.")

def deleteData(cursor):
    cursor.execute("DELETE FROM inventory WHERE name=%(param1)s;", {'param1':"orange"})
    print("Deleted",cursor.rowcount,"row(s) of data.")

