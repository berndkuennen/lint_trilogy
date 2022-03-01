
from flask import Blueprint
from flask import request
from flask import Response, stream_with_context

conv_base64 = Blueprint('conv_base64', __name__)

from yamllint.config import YamlLintConfig
from yamllint import linter

import json
from html import escape

from general import generate_form, generate_head

import base64

# configure yaml linter
conf = YamlLintConfig(file='.yamllint')

#== take the posted text (if any) and lint it
def encodeData():
    # works for key:value POSTs
    data = request.form['data'] # a multidict containing POST data
    try:
      encString = base64.b64encode( data.encode('ascii') ).decode('ascii')
    except:
      encString = "error"
    return encString


#== generate HTML for the editor
def generate_html(data2lint, message, encoded, action):
    html = (generate_head() +
            """<center><h1>b45eG4==</h1>""" +
            generate_form(data2lint, action) +
            """<div class="message">""" + 
            message +
            """</div>""" +
            encoded +
            """</center></body></html>""" )
    return html


#== using editor to lint
@conv_base64.route('/conv/base64/form', methods = ['POST','GET'])
def conv_base64x():
    if request.method == 'GET':
        return generate_html('', '', '', '/conv/base64/form')
    else:
        message = "<h3>Result</h3><p></p>"

        encoded = """
          <div class='container'>
            <div class="line-nums"><button class="copyBtn">&#x1f4cb;</button></div>
            <input class='b64input' id='encodedData' type='text' value='""" + encodeData() + """' />
          </div>
        <br/></p>
        <p>
        Use the button on the left side to copy the data to the clipboard.
        </p>
        <script> addCopyPasteListener(); </script>

        """

        return generate_html( request.form['data'], message, encoded, "/conv/base64/form" )


#== answer POST with JSON
@conv_base64.route('/conv/base64/json', methods = ['POST'])
def conv_base64_json():
    data = {}
    data['encoded'] = encodeData()
    # return pretty printed json
    return Response(stream_with_context(json.dumps(data, indent=4, sort_keys=True)), mimetype='application/json')


#== just give true or false, e.g. for simple bash scripts
@conv_base64.route('/conv/base64/text', methods = ['POST'])
def conv_base64_valid():

    data = encodeData()

    return Response(stream_with_context(data), mimetype='text/plain')

