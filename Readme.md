
# Lint a YAML

## TL;DR
This project provides some tools to lint your YAML or JSON via HTTP requests, including a comfortable form based HTML page and some simple POST interfaces which are returning the result e.g. as JSON or CSV.

## Where to lint my YAML - securely?
I quite often write YAML or JSON  files and I find it handy to check it at (yaml|json)lint.com. But sometimes there's sensible data in the YAML that should not be given to a third party - so I decided to write my own xxxxlint webservice.

Technically it's a flask/uwsgi webserver with some python scripts, based on the tiangolo/uwsgi-nginx-flask docker image. There's a form for comfortably entering and editing the YAML, including automatic resizing and line numbering. 

If you want to use it for automation, e.g. in CI/CD processes, you may use one of the POST interfaces which are answering in JSON, CSV or plain text (see below).

In the future, I want to add more linters (e.g. for XML) or converters (e.g. base64) so this becomes a useful multi purpose tool.

Btw., the name of the project refers to the [Dollars Trilogy](https://en.wikipedia.org/wiki/Dollars_Trilogy).

## Docker
Build an image and run it with the following commands:
```
docker build -t lint_a_yaml .
docker run  -p 80:80  --name lintayaml lint_a_yaml
```

## Credits
This project is based on the valuable work of many other people. Thanks to the following people or organizations:
* Sebastián Ramírez (aka [tiangolo](https://github.com/tiangolo)) for the docker image
* Jacob Kelley for [Behave.js](https://jakiestfu.github.io/Behave.js/) which is the foundation for the [editor](https://embed.plnkr.co/plunk/EKgvbm).


----

## Lint your YAML
These are the interfaces to lint a YAML. Choose one according to your needs.

### /lint/yaml/form
This page offers a comfortable HTML form to enter a YAML and lint it. On clicking the button, the app checks the YAML and gives feedback as an unordered list, or, in best case, tells you that the YAML ist valid.
 
### /lint/yaml/csv
This interface accepts POST requests and awaits the YAML in the field _yaml_. Response is given as CSV list, which remains empty (zero lines) if the YAML is valid.

Example:
```
$ curl -X POST -d 'yaml=xxx '  http://192.168.99.101/lint/yaml/csv
1,1,missing document start "---"
1,4,trailing spaces
```

### /lint/yaml/json
This interface accepts POST requests and awaits the YAML in the field _yaml_. Response is given as JSON structure with the man key "value" as response which is telling with a _true_ or _false_ if the YAMl is valid. If there's errors, you'll find an array with line number, column and description. 

Examples:
```
$ curl -X POST -d 'yaml=---'  http://192.168.99.101/lint/yaml/json
{"valid": true}

$ curl -X POST -d 'yaml=xxx '  http://192.168.99.101/lint/yaml/json
{
    "errors": [
        {
            "column": 1,
            "desc": "missing document start \"---\"",
            "line": 1
        },
        {
            "column": 4,
            "desc": "trailing spaces",
            "line": 1
        }
    ],
    "valid": false
}
```

### /lint/yaml/valid
This interface accepts POST requests and awaits the YAML in the field _yaml_. Response is given as simply _true_ or _false_ in mime-type text/plain.

Example:
```
$ curl -X POST -d 'yaml=---'  http://192.168.99.101/lint/yaml/valid
true
```

----

## Lint your JSON
These are the interfaces to lint a JSON. Choose one according to your needs.

### /lint/json/form
This page offers a comfortable HTML form to enter a JSON and lint it. On clicking the button, the app checks the JSON and gives feedback as an unordered list, or, in best case, tells you that the JSON ist valid.
 
### /lint/json/csv
This interface accepts POST requests and awaits the JSON in the field _json_. Response is given as CSV list, which remains empty (zero lines) if the JSON is valid.

Example:
```
$ curl -X POST -d 'json=xxx '  http://192.168.99.101/lint/json/csv
1,1,missing document start "---"
1,4,trailing spaces
```

### /lint/json/json
This interface accepts POST requests and awaits the JSON in the field _json_. Response is given as JSON structure with the man key "value" as response which is telling with a _true_ or _false_ if the YAMl is valid. If there's errors, you'll find an array with line number, column and description. 

Examples:
```
$ curl -X POST -d 'json=---'  http://192.168.99.101/lint/json/json
{"valid": true}

$ curl -X POST -d 'json=xxx '  http://192.168.99.101/lint/json/json
{
    "errors": [
        {
            "column": 1,
            "desc": "missing document start \"---\"",
            "line": 1
        },
        {
            "column": 4,
            "desc": "trailing spaces",
            "line": 1
        }
    ],
    "valid": false
}
```

### /lint/json/valid
This interface accepts POST requests and awaits the JSON in the field _json_. Response is given as simply _true_ or _false_ in mime-type text/plain.

Example:
```
$ curl -X POST -d 'json=---'  http://192.168.99.101/lint/json/valid
true
```

