import models
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
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



@app.route('/', methods=('GET', 'POST'))
def index(): 
    if request.method == 'GET': 
        return render_template('dashboard.html')

@app.route('/try', methods=('GET', 'POST'))
def index1(): 
    if request.method == 'GET': 
        # score_id = request.args.get('score', type = str)
        # # scores = models.job_score('2546120842')
        # # print('score_id: ',score_id)
        # scores = models.job_score(str(score_id))
        # print('score: ',scores)
        return render_template('try.html')

@app.route('/jobinfo', methods=('GET', 'POST'))
def jobinfo(): 
    if request.method == 'GET': 
        # jobinfo
        title = request.args.get('type', type = str)
        jobinfo = models.jobinfo(title)
        # rec
        selected_job = request.args.get('choosejob', type = str)
        recommend = models.rec(str(selected_job))
        # score
        score_id = request.args.get('score', type = str)
        # score_id = '2528321227'
        score = models.job_score(str(score_id))
        print('score_id: ',score_id)
        print('score: ',score['skills'])
        # print(len(score['skills']))
        # trend
        trend = models.trend()

        # return {'jobinfo':jobinfo,'recommend':recommend,'score':score,'trend':trend} #,'trend':trend
        return {'jobinfo':jobinfo,'recommend':recommend,'score':score}

@app.route('/test', methods=('GET', 'POST'))
def test(): 
    if request.method == 'GET': 
        return render_template('test.html')
                      
if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)