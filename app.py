import etl
import os
from flask import (Flask, g, render_template, flash, redirect, url_for,
                  abort,request,send_from_directory, make_response,json,jsonify)
DEBUG = False
PORT = 3000
HOST = '0.0.0.0'

app = Flask(__name__,
            template_folder='./')

app.secret_key = 'auoesh.bouoastuh.43,uoausoehuosth3ououea.auoub!'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True #排版
app.config['JSON_AS_ASCII'] = False #中文

@app.route('/jobinfo', methods=('GET', 'POST'))
def jobinfo(): 
    if request.method == 'GET': 
        # drop down select, as parameter into next line
        data = etl.jobinfo('data engineer')
        return {'data':data}

# @app.route('/admin/dashboard.html', methods=('GET', 'POST'))
# def dashboard():
#     if request.method == 'GET': 
#         return render_template("midterm.html")

                               
if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)