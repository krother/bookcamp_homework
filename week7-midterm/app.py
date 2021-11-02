"""

file upload done according to the Flask docs: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/ 
"""
from flask import Flask, jsonify, request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from pixpro import train_predict

import os


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask('PixelPro')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # model
            linreg_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'linreg_' + filename)
            tree_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'tree_' + filename)
            train_predict(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'linreg', linreg_filename)
            train_predict(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'tree', tree_filename)

            return redirect(url_for('view_result', linreg_name=linreg_filename, tree_name=tree_filename))
    return render_template('main.html')
    
@app.route('/view_result')
def view_result():
    lr_name = request.args['linreg_name']
    dt_name = request.args['tree_name']
    return render_template('result.html', linreg_filename=lr_name, tree_filename=dt_name)


@app.route('/predict')
def train_and_predict():
    data = {
        'contract': request.args['contract'],
        'tenure': int(request.args['tenure']),
        'monthlycharges': float(request.args['monthlycharges'])
    }
    result = get_prediction(data)
    return jsonify({'churn_proba': result})


