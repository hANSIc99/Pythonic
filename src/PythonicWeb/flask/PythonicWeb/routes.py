import os
from pathlib import Path
from PythonicWeb import PythonicWeb
from flask import render_template, url_for, request, flash
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '~/Pythonic_2019/'
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg' }

PythonicWeb.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
PythonicWeb.config['SECRET_KEY'] = os.urandom(12).hex()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@PythonicWeb.route('/')
@PythonicWeb.route('/index')
def index():
    return render_template('PythonicWeb.html')

"""
    TEST
"""

@PythonicWeb.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        print("test() POST triggered")
        if 'file' not in request.files:
            flash('No file part')
            print('No file part')
            return 'post failed'
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            print('No selected file')
            return 'post failed'
        #if f and allowed_file(f.filename):
        if f:
            # f = werkzeug.datastructures.FileStorage
            # https://werkzeug.palletsprojects.com/en/0.16.x/datastructures/#werkzeug.datastructures.FileStorage
            filename = secure_filename(f.filename)
            print("Filename: {}".format(f.filename))
            #f.save(os.path.join(PythonicWeb.config['UPLOAD_FOLDER'], filename))
            f.save(os.path.join(Path.home(), filename))
            #f.save(PythonicWeb.config['UPLOAD_FOLDER'], filename)
            return 'post successfull'
        else:
            print("No file found")
            return 'No file found'
    else:
        print("test() GET triggered")
        return render_template('test.html')


"""
    LOAD WEBASSEMBLY
"""
@PythonicWeb.route('/qtloader.js')
def qtloader():
    return PythonicWeb.send_static_file('qtloader.js')

@PythonicWeb.route('/qtlogo.svg')
def qtlogo():
    return PythonicWeb.send_static_file('qtlogo.svg')

@PythonicWeb.route('/PythonicWeb.js')
def wasm_glue():
    return PythonicWeb.send_static_file('PythonicWeb.js')

@PythonicWeb.route('/PythonicWeb.wasm')
def wasm_loader():
    return PythonicWeb.send_static_file('PythonicWeb.wasm')

"""
    COMMMUNICATION
"""

@PythonicWeb.route('/test_1', methods=['POST'])
def test_one():
    req_data = request.get_data()
    print("test_one triggered: {}".format(req_data))
    return("Successfull")

@PythonicWeb.route('/upload', methods=['POST'])
def upload():
    print('PythonicWeb.routes upload() called')
    if request.method == 'POST':
        # .get('file') verwenden, wenn nicht vorhanden wir None zurück gegeben
        f = request.files['file']
        print(f.filename)

#print('Language: {}'.format(request.form.get('language')))
#print('Framework: {}'.format(request.form.get('framework')))

