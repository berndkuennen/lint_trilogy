
from flask import Flask
from flask import request

from lint_yaml import lint_yaml
from lint_json import lint_json

from general import generate_form

app  = Flask(__name__)

app.register_blueprint(lint_yaml)
app.register_blueprint(lint_json)


@app.route("/")
def hello():
    return render_main_html()


@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static', 'js'), filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=80)


def render_main_html():
    return """
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
    <img src="/static/img/FistfulOfYaml.jpg" width="120" />
    <h1>Lint trilogy</h1>
    <p>This service offers the possibility to lint data in <a href="/lint/yaml/form">YaML</a> and <a href="/lint/json/form">JSON</a>. A third linter will follow.</p>
""" + generate_form("#\n#place your json or yaml here\n#","") + """

  <br>
  <p align="center" style="font-size:8pt;">(C) 2020 Bernd Künnen - Source on <a href="https://github.com/berndkuennen/lint_trilogy">GitHub</a></p>
  </body>
</html>
"""

