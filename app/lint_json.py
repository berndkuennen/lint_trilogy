
from flask import Blueprint
from flask import request
from flask import Response, stream_with_context

lint_json = Blueprint('lint_json', __name__)

import json
from html import escape

from general import generate_form, generate_head

#== take the posted json (if any) and lint it
def lint_the_json():
    # works for key:value POSTs
    data = request.form['data'] # a multidict containing POST data
    try:
        j = json.loads(data)
        #print("json is valid")
        return []
    except json.JSONDecodeError as err:
        #print("json is invalid")
        error = {}
        error['line']   = err.lineno
        error['column'] = err.colno
        error['desc']   = err.msg
        return [ error ]


#== generate HTML for the editor
def generate_html(data2lint, message, action):
    html = (generate_head()					+
            """<h1>The Good, the Bad and the JSON</h1> """	+
            generate_form(data2lint, action)			+
            """<center><div class="message">"""			+
            message						+
            """</div></center></body></html>"""			)

    return html


#== using editor to lint
@lint_json.route('/lint/json/form', methods = ['POST','GET'])
def lint_jsonx():
    if request.method == 'GET':
        return generate_html('', '', '/lint/json/form')
    else:
        message = "<h3>Result</h3><p>"
        errors = lint_the_json()
        if errors:
            message += "The JSON is <b style='color:red;'>invalid</b>.<br/>Found the following errors in json file:\n<ul>"
            for error in errors:
                message += "<li>Line " + str(error['line']) + ", column " + str(error['column']) + ": " + escape(error['desc']) + "\n"
            message += "</ul>"
            data4form = request.form['data']
        else:
            message += "The JSON is <b style='color:green;'>valid</b>.\n"
            data4form = json.dumps( json.loads(request.form['data']), indent=4, sort_keys=True )
        message += "</p>"

        return generate_html( data4form, message, "/lint/json/form" )


#== answer POST with JSON
@lint_json.route('/lint/json/json', methods = ['POST'])
def lint_json_json():
    data = {}

    errors = lint_the_json()
    if errors:
        data['valid']  = False
        data['errors'] = []
        for error in errors:
            err = {}
            err['line']   = error['line']
            err['column'] = error['column']
            err['desc']   = error['desc']
            data['errors'].append( err )
    else:
        data['valid'] = True
    # return pretty printed json
    return Response(stream_with_context(json.dumps(data, indent=4, sort_keys=True)), mimetype='application/json')


#== answer POST with CSV (zero lines means valid json)
@lint_json.route('/lint/json/csv', methods = ['POST'])
def lint_json_csv():
    data = ""
    errors = lint_the_json()
    if errors:
        for error in errors:
            data += str(error['line'])   + ","
            data += str(error['column']) + ","
            data +=     error['desc']    + "\n"
    return Response(stream_with_context(data), mimetype='text/csv')


#== just give true or false, e.g. for simple bash scripts
@lint_json.route('/lint/json/valid', methods = ['POST'])
def lint_json_valid():
    errors = lint_the_json()
    if errors:
      data = "false"
    else:
      data = "true"
    return Response(stream_with_context(data), mimetype='text/plain')

