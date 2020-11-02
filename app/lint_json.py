
from flask import Blueprint
from flask import request
from flask import Response, stream_with_context

lint_json = Blueprint('lint_json', __name__)

import json
from html import escape

#== take the posted json (if any) and lint it
def lint_the_json():
    # works for key:value POSTs
    data = request.form['json'] # a multidict containing POST data
    try:
        j = json.loads(data)
        #print("json is valid")
        return []
    except json.JSONDecodeError as err:
        #print("json is invalid")
        #print(str(err.lineno) + "," + str(err.colno) + ": " + err.msg )
        #lines = str.splitlines(data)
        #print(lines[err.lineno-1])
        error = {}
        error['line']   = err.lineno
        error['column'] = err.colno
        error['desc']   = err.msg
        return [ error ]


#== generate HTML for the editor
def generate_form(json2lint, message):
    html = """
<!DOCTYPE html>
<html>

  <head>
    <!-- script data-require="angularjs@1.3.6" data-semver="1.3.6" src="//cdnjs.cloudflare.com/ajax/libs/angular.js/1.3.6/angular.min.js"></script -->
    <script data-require="angularjs@1.3.6" data-semver="1.3.6" src="/static/js/angular.min.js"></script>
    <link rel="stylesheet" href="/static/style.css" />
    <script type="text/javascript" src="/static/js/behave.js"></script>
    <script type="text/javascript" src="/static/js/script.js"></script>
  </head>

  <body>
        <a href="/"><img src="/static/img/FistfulOfYaml.jpg" width="40" /></a><h1>The Good, the Bad and the JSON</h1>
	
	<form action="/lint/json/form" method="POST">

	<!-- autonumber & resize example inspired by https://embed.plnkr.co/plunk/EKgvbm -->
	<div class="container">
		<div class="line-nums"><span>1</span></div>
		<textarea id="editor" name="json" autofocus >""" + escape(json2lint) +"""</textarea>
	</div>
	<br/>
	<input type="submit" />
	
        </form>
        <center><div class="message">""" + message + """</div></center>
  </body>

</html>

"""
    return html


#== using editor to lint
@lint_json.route('/lint/json/form', methods = ['POST','GET'])
def lint_jsonx():
    if request.method == 'GET':
        return generate_form("{\n  \"key\": \"enter your json here\"\n}","")
    else:
        message = "<h3>Result</h3><p>"
        errors = lint_the_json()
        if errors:
            message += "The JSON is <b style='color:red;'>invalid</b>.<br/>Found the following errors in json file:\n<ul>"
            for error in errors:
                message += "<li>Line " + str(error['line']) + ", column " + str(error['column']) + ": " + escape(error['desc']) + "\n"
            message += "</ul>"
        else:
            message += "The JSON is <b style='color:green;'>valid</b>.\n"
        message += "</p>"

        return generate_form( request.form['json'], message )


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

