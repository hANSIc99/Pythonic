from PythonicWeb import PythonicWeb
from flask import render_template, url_for, request

@PythonicWeb.route('/')
@PythonicWeb.route('/index')
def index():
    return render_template('PythonicWeb.html')

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
        f = request.files['file']
        print(f.filename)

