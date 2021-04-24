
from sqlite3.dbapi2 import Error
from typing import OrderedDict
from flask import Flask, request, render_template, url_for, redirect, Response, jsonify
import os
from werkzeug.utils import secure_filename
import csv
import json
from pandas import read_csv
import sqlite3 as sql
from itertools import zip_longest
import requests
app = Flask(__name__)



service_1 = []
service_2 = []
js = []

csvpath = os.listdir('csv')
for f in csvpath:
    os.remove(os.path.join('csv', f))


@app.route('/')

def upload():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    count = 0
 

    db_name ='csv/csvtest_{}.db'

            

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
        cur.execute('ALTER TABLE dita ADD COLUMN BVN STRING')
        cur.execute('UPDATE dita SET FULLNAME = (FIRSTNAME|| " " || SURNAME)')
        cur.execute('SELECT EMAIL, DEVICE_ID, CLIENT_ID, ID, PHONE, IFNULL(BVN,"NULL") AS BVN, FULLNAME FROM dita')
        rows =cur.fetchall()
        ki = []
        di = []

        for row in rows:
            k = {}
            le = {}

            d = {}
            le['username'] = row[0]
            d['customer_rank'] = row[1]
            d['phone'] = row[4]
            d['fullname'] = row[6]
            d['email'] = row[0]

            response = requests.post(url="http://localhost:5000/service_1", data=d)
            

            y = response.json()
            z = y['model']['id']
            d['customer']= z 

            claim1 = {'claim':"http://wso2.org/claims/deviceid", "value":row[1]}
            claim2 = {'claim':"http://wso2.org/claims/externalid", "value":row[2]}
            claim3 = {'claim':"http://wso2.org/claims/customerid", "value":row[3]}
            claim4 = {'claim':"http://wso2.org/claims/userid", "value":z}
            claim5 = {'claim':"http://wso2.org/claims/mobile", "value":row[4]}
            claim6 = {'claim':"http://wso2.org/claims/askPassword", "value":0}
            claim7 = {'claim':"http://wso2.org/claims/emailVerified", "value":1}
            claim8 = {'claim':"http://wso2.org/claims/preferredChannel", "value":"EMAIL"}
            claim9 = {'claim':"http://wso2.org/claims/phoneVerified", "value":1}
            claim10 = {'claim':"http://wso2.org/claims/extendedExternalId", "value":row[5]}

            properties = [claim1,claim2, claim3, claim4, claim5, claim6, claim7, claim8, claim9, claim10]
            le['properties'] = properties
            
            #call service 1 and assign values
            service_1.append(d)
            service_2.append(le)
            
            response2 = requests.post(url="http://localhost:5000/service_2", data=service_2)
            

            # print(response.json())
            
       #     ki.append(row[3])
        # print(response)

        # servic = [{a:b} for (a,b) in zip_longest(ki,di)]
        # service_1.append(servic)
        

        # with open('jsondump/1stcall.json', 'w') as jss:
        #     json.dump(service_1, jss)
        conn.close()


        #  delete all files in /csv
        return jsonify({'row': response2.json()})

@app.route('/service_1', methods=['POST'])
def returnAll():
    return ({'model':{'id':99}})

@app.route('/service_1', methods=['GET'])
def returnOne(name):
    the_one = service_1[0]
    for i, q in enumerate(service_1):
        if q ['name'] ==  name:
            the_one = service_1[i]
        return jsonify({'service_1': service_1})

@app.route('/service_2', methods=['POST'])
def return_ser_2():
    return request.get_data()

# @app.route('/service_1', methods=['GET'])
# def returnOne(name):
#     the_one = service_1[0]
#     for i, q in enumerate(service_1):
#         if q ['name'] ==  name:
#             the_one = service_1[i]
#         return jsonify({'service_1': service_1})






if __name__ == "__main__":
    app.run(debug=True)
