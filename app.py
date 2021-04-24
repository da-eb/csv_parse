
from sqlite3.dbapi2 import Error
from typing import OrderedDict
from flask import Flask, request, render_template, url_for, redirect, Response, jsonify
import os
from werkzeug.utils import secure_filename
import csv
import codecs
import json
from pandas import read_csv
import sqlite3 as sql
from itertools import zip_longest

app = Flask(__name__)



service_1 = []
js = []



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
        cur.execute('ALTER TABLE dita ADD COLUMN FULLNAME STRING')
        cur.execute('ALTER TABLE dita ADD COLUMN CUSTOMER_RANK STRING')
        cur.execute('UPDATE dita SET FULLNAME = (FIRSTNAME|| " " || SURNAME)')
        cur.execute('SELECT FULLNAME, CUSTOMER_RANK, PHONE, EMAIL FROM dita')
        rows =cur.fetchall()
        ki = []
        di = []

        for row in rows:
            d = {}
            d['customer_rank'] = row[1]
            d['mobile'] = row[2]
            d['fullname'] = row[0]
            di.append(d)
            
            ki.append(row[3])
        print(di)

        servic = [{a:b} for (a,b) in zip_longest(ki,di)]
        service_1.append(servic)
        # response = req.post("http://localhost:5000/service_1", service_1)

        with open('jsondump/1stcall.json', 'w') as jss:
            json.dump(service_1, jss)
        conn.close()

        return jsonify({'service_1': service_1})


   
@app.route('/service_1', methods=['POST'])
def returnAll():
    return jsonify({'service_1':service_1})

@app.route('/service_1', methods=['GET'])
def returnOne(name):
    the_one = service_1[0]
    for i, q in enumerate(service_1):
        if q ['name'] ==  name:
            the_one = service_1[i]
        return jsonify({'service_1': service_1})



if __name__ == "__main__":
    app.run(debug=True)
