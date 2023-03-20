from flask import Flask, jsonify, request, redirect, url_for, render_template
import psycopg2
import random
from config import config

app = Flask(__name__)

try:
    params = config()
    print('Connecting to database...')
    connection = psycopg2.connect(**params)
    connection.autocommit = True
    cursor = connection.cursor()
    print('PostgreSQL DB version: ')
    cursor.execute('SELECT version()')
    db_version = cursor.fetchone()
    print(db_version)
except(Exception, psycopg2.DatabaseError) as error:
    print(error)

data = []


@app.route("/home")
def homepage():
    return render_template("index.html")


@app.route('/mispisit_db', methods=['GET'])
def users_get():
    sql = 'SELECT * FROM users;'
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template("users.html", data = data)


@app.route('/mispisit_db/<userid>', methods=['GET'])
def userid_get():
    sql = 'SELECT * FROM mispisit_db WHERE id = %s'
    cursor.execute(sql, (str(),) )
    data = cursor.fetchall()
    print(data)
    return data


@app.route('/mispisit_db', methods=['POST'])
def user_add():
    sql = 'INSERT INTO mispisit_db VALUES (%s, %s ,%s)'
    id = random.randint(0, 100000)
    req_data = request.json['req_data']
    report_info = request.json['report_info']
    other_info = request.json['other_info']
    cursor.execute(sql, (id, req_data, report_info, other_info))
    connection.commit()
    return userid_get(id), data


@app.route('/mispisit_db', methods=['DELETE'])
def user_del():
    data.pop(request.get_json()['id'])
    return data


@app.route('/mispisit_db', methods=['PUT'])
def user_upd():
    updsql = """ UPDATE users
                    SET req_data = %s
                    SET report_info = %s
                    SET other_info = %s
                    WHERE id = %s"""
    id = request.json['id']
    req_data = request.json['req_data']
    report_info = request.json['report_info']
    other_info = request.json['other_info']
    cursor.execute(updsql, (id, req_data, report_info, other_info))
    return data

if __name__ == '__main__':
    app.run(debug=True)
