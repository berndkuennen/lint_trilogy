
![Lint Trilogy Logo](Lint_Trilogy_200px.jpg)

# Lint Trilogy

## TL;DR
This project provides some tools to lint your YAML, XML or JSON via HTTP requests, including a comfortable form based HTML editor and some simple POST interfaces which are returning the result e.g. as JSON or CSV.

## Where to lint my YAML/XML/JSON - safely?
I quite often write YAML or JSON  files and I find it handy to check it at (yaml|json)lint.com. But sometimes there's sensible data in the YAML that should not be given to a third party - so I decided to write my own xxxxlint webservice.

Technically it's a flask/uwsgi webserver with some python scripts, based on the [tiangolo/uwsgi-nginx-flask](https://github.com/tiangolo/uwsgi-nginx-flask-docker) docker image. There's a form for comfortably entering and editing the YAML/XML/JSON, including automatic resizing and line numbering. You may try it out on the <a href="https://www.lint-trilogy.com/">demo page</a>. But please don't use it regularly but build your own linter based on this code or the docker image.

If you want to use it for automation, e.g. in CI/CD processes, you may use one of the POST interfaces which are answering in JSON, CSV or plain text (see below).

In the future, I want to add more linters or converters (e.g. base64) so that this could become a useful multi purpose tool.

Btw., the name of the project refers to the [Dollars Trilogy](https://en.wikipedia.org/wiki/Dollars_Trilogy).

## Credits
This project is based on the valuable work of many other people. Thanks to the following people or organizations:
* Sebastián Ramírez (aka [tiangolo](https://github.com/tiangolo)) for the docker image
* Jacob Kelley for [Behave.js](https://jakiestfu.github.io/Behave.js/) which is the foundation for the [editor](https://embed.plnkr.co/plunk/EKgvbm).
* Francesco Linza for improving the Javascript editor code.

## Licensing
The code is under [MIT license](License.txt). The lint trilogy logo is under CC BY-SA 4.0.

---

## Docker
Build an image and run it with the following commands:
```
docker build -t lint_trilogy .
docker run  -p 80:8080  --name eastwood lint_trilogy
```

Ready to go images may be found on [docker hub](https://hub.docker.com/repository/docker/docdiesel/lint_trilogy). For running docdiesel/lint_trilogy on kubernetes, please refer to the sample [deployment.yml](deployment.yml). Note: Due to the restrictions that OpenShift/OKD have regarding containers running as root it's not possible _yet_ to run lint_trilogy on these platforms.

----

## A Fistful of YAML
These are the interfaces to lint a YAML. Choose one according to your needs.

### /lint/yaml/form
This page offers a comfortable HTML form to enter a YAML and lint it. On clicking the button, the app checks the YAML and gives feedback as an unordered list, or, in best case, tells you that the YAML ist valid.
 
### /lint/yaml/csv
This interface accepts POST requests and awaits the YAML in the field _data2lint_. Response is given as CSV list (content type text/csv), which remains empty (zero lines) if the YAML is valid.

Example:
```
$ curl -X POST -d 'data2lint=xxx '  http://192.168.99.101/lint/yaml/csv
1,1,missing document start "---"
1,4,trailing spaces
```

### /lint/yaml/json
This interface accepts POST requests and awaits the YAML in the field _data2lint_. Response is given as JSON structure (content type application/json) with the man key "value" as response which is telling with a _true_ or _false_ if the YAMl is valid. If there's errors, you'll find an array with line number, column and description. 

Examples:
```
$ curl -X POST -d 'data2lint=---'  http://192.168.99.101/lint/yaml/json
{"valid": true}

$ curl -X POST -d 'data2lint=xxx '  http://192.168.99.101/lint/yaml/json
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
This interface accepts POST requests and awaits the YAML in the field _data2lint_. Response is given as simply _true_ or _false_ (content type text/plain).

Example:
```
$ curl -X POST -d 'data2lint=---'  http://192.168.99.101/lint/yaml/valid
true
```

----

## For a Few XML More
These are the interfaces to lint a XML. Choose one according to your needs. Error details reporting is not implemented _yet_.

### /lint/xml/form
This page offers a comfortable HTML form to enter a XML and lint it. On clicking the button, the app checks the XML and gives feedback as an unordered list (to be implemented), or, in best case, tells you that the XML is valid.
 
### /lint/xml/csv
This interface accepts POST requests and awaits the XML in the field _data2lint_. Response is given as CSV list (content type text/csv), which remains empty (zero lines) if the XML is valid.

Example:
```
$ curl -X POST -d 'data2lint=<xml>no</yaml>'  http://192.168.99.101/lint/xml/csv
0,0,error reporting not yet implemented
```

### /lint/xml/json
This interface accepts POST requests and awaits the XML in the field _data2lint_. Response is given as JSON structure (content type application/json) with the main key "valid" as response which is giving you the result _true_ or _false_. If there's errors, you'll find an array with line number, column and description (to be implemented). 

Examples:
```
$ curl -X POST -d 'data2lint=<xml></xml>'  http://192.168.99.101/lint/xml/json
{"valid": true}

$ curl -X POST -d 'data2lint=<this>is no<xml>'  http://192.168.99.101/lint/xml/json
{
    "errors": [
        {
            "column": 0,
            "desc": "error reporting not yet implemented",
            "line": 0
        }
    ],
    "valid": false
}
```

### /lint/xml/valid
This interface accepts POST requests and awaits the XML in the field _data2lint_. Response is given as simply _true_ or _false_ (content type text/plain).

Example:
```
$ curl -X POST -d 'data2lint=<this>is no<xml>'  http://192.168.99.101/lint/xml/valid
false
```

----

## The Good, the Bad and the JSON
These are the interfaces to lint a JSON. Choose one according to your needs. The basic python json library stops at the first error so you always get a list/array with just the next error as answer.

### /lint/json/form
This page offers a comfortable HTML form to enter a JSON and lint it. On clicking the button, the app checks the JSON and gives feedback as an unordered list, or, in best case, tells you that the JSON ist valid.
 
### /lint/json/csv
This interface accepts POST requests and awaits the JSON in the field _data2lint_. Response is given as CSV list (content type text/csv), which remains empty (zero lines) if the JSON is valid.

Example:
```
$ curl -X POST -d 'data2lint={ "this": is no json }'  http://192.168.99.101/lint/json/csv
1,11,Expecting value
```

### /lint/json/json
This interface accepts POST requests and awaits the JSON in the field _data2lint_. Response is given as JSON structure (content type application/json) with the main key "valid" as response giving you the result _true_ or _false_. If there's errors, you'll find an array with line number, column and description. 

Examples:
```
$ curl -X POST -d 'data2lint={}'  http://192.168.99.101/lint/json/json
{"valid": true}

$ curl -X POST -d 'data2lint={ "this": is no json }'  http://192.168.99.101/lint/json/json
{
    "errors": [
        {
            "column": 11,
            "desc": "Expecting value",
            "line": 1
        }
    ],
    "valid": false
}
```

### /lint/json/valid
This interface accepts POST requests and awaits the JSON in the field _data2lint_. Response is given as simply _true_ or _false_ (content type text/plain).

Example:
```
$ curl -X POST -d 'data2lint={ "this": is no json }'  http://192.168.99.101/lint/json/csv
false
```

