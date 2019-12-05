#importing libraries
import os
import numpy as np
import flask
from sklearn.ensemble import RandomForestClassifier
import pickle
from flask import Flask, render_template, redirect, url_for, request
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import pandas as pd
from sklearn.externals import joblib
from flask_sqlalchemy import SQLAlchemy
#creating instance of the class
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploaded/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['csv'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/upload', methods=['POST'])
def predict():
    source_dir = "uploaded/"

    for file in os.listdir(source_dir):
        data_files=pd.read_csv(file)
        data=data_files.iloc[:,  0:data_files.shape[1]]
        loaded_model = joblib.load("modeldengue.pkl")
        prediction = loaded_model.predict(data)
    return render_template("result.html", predictions=prediction)

if __name__=="__main__":
    app.run(debug=True)