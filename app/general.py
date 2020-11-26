

from flask import request
from html  import escape


#== generate HTML for the editor
def generate_form(data2lint, action):

    # check whether we are in lint or in conv branch
    module = request.path.split('/')[1]

    form = """
	<form action=\"""" + action + """\" method="POST">

	<!-- autonumber & resize example inspired by https://embed.plnkr.co/plunk/EKgvbm -->
	<div class="container">
		<div class="line-nums"><span>1</span></div>
		<textarea id="editor" name="data" autofocus
		placeholder="place your yaml/xml/json here">""" + escape(data2lint) + """</textarea>
	</div>
	<br/>\n"""

    if action == "":

      if module == 'lint' or module == '' :
        form += """
          <input type="submit" value="Lint YAML" onclick="javascript: form.action='/lint/yaml/form';">
          <input type="submit" value="Lint XML"  onclick="javascript: form.action='/lint/xml/form';" >
          <input type="submit" value="Lint JSON" onclick="javascript: form.action='/lint/json/form';"> \n"""

      if module == 'conv':
        form += """
          <input type="submit" value="base64"       onclick="javascript: form.action='/conv/base64/form'; ">
          <input type="button" value="base64/gzip"  onclick="javascript: alert('Function not implemented yet'); ">
          <input type="button" value="base64/bzip2" onclick="javascript: alert('Function not implemented yet'); ">\n"""

    else:

      if module == 'lint':
        form += """<input type="submit" value="Lint"/>&nbsp;"""

      form += """<input type="submit" value="Encode"  onclick="javascript: form.action='/conv/base64/form';" >\n"""

    form += """
        </form>\n"""
    return form


#== generate HEAD etc =======================
def generate_head():
    html = """<!DOCTYPE html>
<html>

  <head>
    <!-- script data-require="angularjs@1.3.6" data-semver="1.3.6" src="//cdnjs.cloudflare.com/ajax/libs/angular.js/1.3.6/angular.min.js"></script -->
    <script data-require="angularjs@1.3.6" data-semver="1.3.6" src="/static/js/angular.min.js"></script>
    <link rel="stylesheet" href="/static/style.css" />
    <script type="text/javascript" src="/static/js/behave.js"></script>
    <script type="text/javascript" src="/static/js/script.js"></script>
    <title>Lint Trilogy - The YAML, the XML and the JSON</title>
  </head>

  <body>
        <a href="/"><img src="/static/img/FistfulOfYaml.jpg" width="40" /></a>
        """
    return html
