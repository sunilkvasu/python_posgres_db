#!/usr/bin/python3
#
# - Python module update the patchengine database
# - To Insert data use: http://<hostname>:<port>/insert/<token>/<time>/<server>/<change>/<own>/<app>/<status>
# - To Update table use: http://<hostname>:<port>/update/<token>/<time>/<server>/<change>/<own>/<app>/<status>
# - Ensure the pip modules installed: flask, dotenv, psycopg2, os
# - Author: Sunil Kamba Vasu(sunilkamba.vasu@flex.com)
#


# - Importing required libraries
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv, dotenv_values
import psycopg2
import os
import logging

logging.basicConfig(filename="patchengine.log", level=logging.INFO)

# - App intializing
app = Flask(__name__)

# - Loading environment variables
load_dotenv()
token_id = os.getenv('token_id')
pg_db = os.getenv('pg_db')
pg_user = os.getenv('pg_user')
pg_pass = os.getenv('pg_pass')
pg_host = os.getenv('pg_host')
pg_port = os.getenv('pg_port')

# - Error handling
invalid_status = 'ERROR: Not a valid status code!!!'
not_authourized = 'ERROR: Invalid token ID. Not authorized to perform this operation'
insert_successful = 'INFO: Data Inserted succesfully'
update_successful = 'INFO: Data Updated succesfully'
insert_fail = 'ERROR: Could not insert this data. Kindly check for duplicates!!!'
update_fail = 'ERROR: Could not update table'

# - Connecting to postgres DB
connection_params = {
        'dbname': pg_db,
        'user': pg_user,
        'password': pg_pass,
        'host': pg_host,
        'port': pg_port
        }
connection = psycopg2.connect(**connection_params)
cursor = connection.cursor()

# - Creating insert route
@app.route('/insert/<token>/<time>/<server>/<change>/<own>/<app>/<status>')
def insert(token, time, server, change, own, app, status):
    statusd = ['unscheduled', 'scheduled', 'started', 'patched', 'failed']
    if status not in statusd:
        print(invalid_status)
        retJson = {
                "Status": invalid_status
                }
        logging.error(invalid_status)
        return jsonify(retJson)
    else:
        if token != token_id:
            print(not_authourized)
            retJson = {
                    "Status": not_authourized
                }
            logging.error(not_authourized)
            return jsonify(retJson)
        else:
            connection_params = {
            'dbname': pg_db,
            'user': pg_user,
            'password': pg_pass,
            'host': pg_host,
            'port': pg_port
            }
            connection = psycopg2.connect(**connection_params)
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO patchdata (timestamp, server_id, change_id, ownemail, appemail, status_code) VALUES(%s, %s, %s, %s, %s, %s)", (time, server, change, own, app, status))
                connection.commit()
                retJson = {
                    "timestamp": time,
                    "server_id": server,
                    "change_id": change,
                    "ownemail": own,
                    "appemail": app,
                    "status_code": status
                    }
                print(insert_successful)
                logging.info(insert_successful)
            except psycopg2.Error as error:
                print(insert_fail)
                logging.error(insert_fail)
                print(error)
                retJson = {
                        "Status": insert_fail,
                        }
            cursor.close()
            connection.close()
            return jsonify(retJson)

# - Creating update route
@app.route('/update/<token>/<time>/<server>/<change>/<own>/<app>/<status>')
def update(token, time, server, change, own, app, status):
    statusd = ['unscheduled', 'scheduled', 'started', 'patched', 'failed']
    if status not in statusd:
        print(invalid_status)
        logging.error(invalid_status)
        retJson = {
            "Status": invalid_status
            }
        return jsonify(retJson)
    else:
        if token != token_id:
            print(not_authourized)
            logging.error(not_authourized)
            retJson = {
                "Status": not_authourized
                }
            return jsonify(retJson)
        else:
            connection_params = {
            'dbname': pg_db,
            'user': pg_user,
            'password': pg_pass,
            'host': pg_host,
            'port': pg_port
            }
            connection = psycopg2.connect(**connection_params)
            cursor = connection.cursor()
            update_query = """UPDATE patchdata SET status_code = %s WHERE timestamp = %s"""
            data_to_update = (status, time)
            try:
                cursor.execute(update_query, data_to_update)
                connection.commit()
                retJson = {
                    "timestamp": time,
                    "server_id": server,
                    "change_id": change,
                    "ownemail": own,
                    "appemail": app,
                    "status_code": status
                    }
                print(update_successful)
                logging.info(update_successful)
            except psycopg2.Error as error:
                print(update_fail)
                logging.error(update_fail)
                print(error)
                retJson = {
                    "Status": update_fail,
                    }
            cursor.close()
            connection.close()
            return jsonify(retJson)

# - creating reporting route
@app.route('/patch/report')
def report():
    cursor.execute("""SELECT * FROM patchdata""")
    rep = cursor.fetchall()
    return render_template('report.html', report = rep)

# - Main program
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="4210")
