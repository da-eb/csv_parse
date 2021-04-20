

from sqlite3.dbapi2 import Error
from flask import Flask, request, render_template, url_for, redirect, Response, jsonify
import os
from werkzeug.utils import secure_filename
import csv
import json
import codecs
from pandas import read_csv
import sqlite3 as sql


app = Flask(__name__)

@app.route('/')


def upload():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    count = 0
    db_name ='csvtest_{}.db'

    while os.path.isfile(db_name.format(count)):
        count +=1
    db_name = db_name.format(count)

    if request.method == 'POST':
        f = request.files['file']
        data = []

        conn = sql.connect(db_name )
        dita = read_csv(f)
        dita.to_sql('dita', conn)

        cur = conn.cursor()
        cur.execute("SELECT FIRSTNAME, SURNAME FROM dita")
        rows = cur.fetchall()
        for row in rows:
            print (row)
        conn.close()

        
        
        return 'success'


if __name__ == "__main__":
    app.run(debug=True)



        # stream = codecs.iterdecode(f.stream, 'utf-8')
        # for rows in csv.reader(stream, dialect=csv.excel):
        #     if rows:
        #         data.append(rows)

        #         headers = data[0]
        #         dat = data[1:]
  
        # return render_template('table.html', headers = headers, dat=dat )
