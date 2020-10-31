
from flask import Flask
from flask import request

from lint_yaml import lint_yaml
from lint_json import lint_json

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
    <link rel="stylesheet" href="/static/style.css" />
  </head>

  <body>
    <img src="/static/img/FistfulOfYaml.jpg" width="120" />
    <h1>Lint trilogy</h1>
    This service offers the possibility to lint data in <a href="/lint/yaml/form">YaML</a> and <a href="/lint/json/form">JSON</a>. A third linter will follow.
  </body>
</html>
"""
