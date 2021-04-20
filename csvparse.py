import csv

# class Csv_parse():

def csv_parse(target):
    with open(target, newline="" ) as csv_file:
        parse = csv.reader(csv_file, delimiter=' ', quotechar = '|')
        for row in parse:
            print(', '.join(row))


fhand = 'CSV_TEST.csv'

csv_parse(fhand)



from flask import Flask, request, render_template, url_for, redirect, Response, jsonify
import os
from werkzeug.utils import secure_filename
import csv
import json
import codecs


app = Flask(__name__)

@app.route('/')

def upload():
    return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']

        data = []

        stream = codecs.iterdecode(f.stream, 'utf-8')
        for rows in csv.reader(stream, dialect=csv.excel):
            if rows:
                data.append(rows)

                headers = data[0]
                dat = data[1:]

            render_template('table.html', headers = headers, dat=dat )
        return True;


if __name__ == "__main__":
    app.run(debug=True)