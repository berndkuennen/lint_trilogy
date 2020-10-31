
from flask import Blueprint
from flask import request
from flask import Response, stream_with_context

lint_yaml = Blueprint('lint_yaml', __name__)

from yamllint.config import YamlLintConfig
from yamllint import linter

import json

# configure yaml linter
conf = YamlLintConfig(file='.yamllint')

#== take the posted yaml (if any) and lint it
def lint_the_yaml():
    # works for key:value POSTs
    data = request.form['yaml'] # a multidict containing POST data

    # for binary upload, not properly working:
    #data = request.files['yaml'] # .read()
    return list(linter.run(data, conf))


#== generate HTML for the editor
def generate_form(yaml2lint, message):
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
        <a href="/"><img src="/static/img/FistfulOfYaml.jpg" width="40" /></a><h1>A Fistful of YAML</h1>
	
	<form action="/lint/yaml/form" method="POST">

	<!-- autonumber & resize example inspired by https://embed.plnkr.co/plunk/EKgvbm -->
	<div class="container">
		<div class="line-nums"><span>1</span></div>
		<textarea id="editor" name="yaml" autofocus >""" + yaml2lint +"""</textarea>
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
@lint_yaml.route('/lint/yaml/form', methods = ['POST','GET'])
def lint_yamlx():
    if request.method == 'GET':
        return generate_form("---\nkey: \"enter your yaml here\"","")
    else:
        message = "<h3>Result</h3><p>"
        errors = lint_the_yaml()
        if errors:
            message += "The YaML is <b style='color:red;'>invalid</b>.<br/>Found the following errors in yaml file:\n<ul>"
            for error in errors:
                message += "<li>Line " + str(error.line) + ", column " + str(error.column) + ": " + error.desc + "\n"
            message += "</ul>"
        else:
            message += "The YaML is <b style='color:green;'>valid</b>.\n"
        message += "</p>"

        return generate_form( request.form['yaml'], message )


#== answer POST with JSON
@lint_yaml.route('/lint/yaml/json', methods = ['POST'])
def lint_yaml_json():
    data = {}

    errors = lint_the_yaml()
    if errors:
        data['valid']  = False
        data['errors'] = []
        for error in errors:
            err = {}
            err['line']   = error.line
            err['column'] = error.column
            err['desc']   = error.desc
            data['errors'].append( err )
    else:
        data['valid'] = True
    # return pretty printed json
    return Response(stream_with_context(json.dumps(data, indent=4, sort_keys=True)), mimetype='application/json')


#== answer POST with CSV (zero lines means valid yaml)
@lint_yaml.route('/lint/yaml/csv', methods = ['POST'])
def lint_yaml_csv():
    data = ""

    errors = lint_the_yaml()
    if errors:
        for error in errors:
            data += str(error.line)   + ","
            data += str(error.column) + ","
            data += error.desc + "\n"

    return Response(stream_with_context(data), mimetype='text/csv')


#== just give true or false, e.g. for simple bash scripts
@lint_yaml.route('/lint/yaml/valid', methods = ['POST'])
def lint_yaml_valid():

    errors = lint_the_yaml()
    if errors:
      data = "false"
    else:
      data = "true"
    
    return Response(stream_with_context(data), mimetype='text/plain')

