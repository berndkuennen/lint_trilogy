
![Lint Trilogy Logo](Lint_Trilogy_200px.jpg)

# Lint Trilogy

## TL;DR
This project provides some tools to lint your **YAML**, **XML** or **JSON** via HTTP requests, including a comfortable form based HTML editor and some simple POST interfaces which are returning the result e.g. as JSON or CSV. Furthermore it offers the possibility to encode the (linted) data to **base64**.

## Where to lint my YAML/XML/JSON - safely?
I quite often write YAML or JSON  files and I find it handy to check it at (yaml|json)lint.com. But sometimes there's sensible data in the YAML that should not be given to a third party - so I decided to write my own xxxxlint webservice.

Technically it's a flask/uwsgi webserver with some python scripts, based on the [tiangolo/uwsgi-nginx-flask](https://github.com/tiangolo/uwsgi-nginx-flask-docker) docker image. There's a form for comfortably entering and editing the YAML/XML/JSON, including automatic resizing and line numbering. You may try it out on the <a href="https://www.lint-trilogy.com/">demo page</a>. But please don't use it regularly but build your own linter based on this code or the docker image.

If you want to use it for automation, e.g. in CI/CD processes, you may use one of the POST interfaces which are answering in JSON, CSV or plain text (see below).

In the future, I want to add more linters or converters (e.g. base64&gzip) so that this could become a useful multi purpose tool.

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

Read more about the functionality of the several modules in the following
documents.

## Linting data
* [A Fistful of YAML](Docs/lint_yaml.md)
* [For a Few XML More](Docs/lint_xml.md)
* [The Good, the Bad and the JSON](Docs/lint_json.md)

## Converting data
* [Base64 Rider](Docs/conv_base64.md)

