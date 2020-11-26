
from flask import Blueprint
from flask import request
from flask import Response, stream_with_context

lint_xml = Blueprint('lint_xml', __name__)

from lxml import etree
from io   import StringIO

import json
from html import escape

from general import generate_form, generate_head


#== take the posted xml (if any) and lint it
def lint_the_xml():
    # works for key:value POSTs
    data = request.form['data'] # a multidict containing POST data

    if data == "" :
        error = {}
        error['line']   = 1
        error['column'] = 1
        error['desc']   = "Expecting value"
        return [ error ]

    try:
        doc = etree.parse(StringIO(data))
        return []

    except etree.XMLSyntaxError as err:
        error = {}
        error['line']   = err.lineno
        error['column'] = err.offset
        error['desc']   = err.msg
        return [ error ]


#== generate HTML for the editor
def generate_html(data2lint, message, action):
    html = (generate_head()			+
            """<h1>For a Few XML More</h1> """	+
            generate_form(data2lint, action)	+
            """<center><div class="message">"""	+
            message				+
            """</div></center></body></html>"""	)

    return html


#== using editor to lint
@lint_xml.route('/lint/xml/form', methods = ['POST','GET'])
def lint_xmlx():
    if request.method == 'GET':
        return generate_html("", "", "/lint/yaml/form")
    else:
        message = "<h3>Result</h3><p>"
        errors = lint_the_xml()
        if errors:
            message += "The XML is <b style='color:red;'>invalid</b>.<br/>Found the following errors in xml file:\n<ul>"
            for error in errors:
                message += "<li>Line " + str(error['line']) + ", column " + str(error['column']) + ": " + escape(error['desc']) + "\n"
            message += "</ul>"
        else:
            message += "The XML is <b style='color:green;'>valid</b>.\n"
        message += "</p>"

        return generate_html( request.form['data'], message, "/lint/xml/form" )


#== answer POST with JSON
@lint_xml.route('/lint/xml/json', methods = ['POST'])
def lint_xml_json():
    data = {}

    errors = lint_the_xml()
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


#== answer POST with CSV (zero lines means valid xml)
@lint_xml.route('/lint/xml/csv', methods = ['POST'])
def lint_xml_csv():
    data = ""

    errors = lint_the_xml()
    if errors:
        for error in errors:
            data += str(error['line'])   + ","
            data += str(error['column']) + ","
            data += error['desc'] + "\n"

    return Response(stream_with_context(data), mimetype='text/csv')


#== just give true or false, e.g. for simple bash scripts
@lint_xml.route('/lint/xml/valid', methods = ['POST'])
def lint_xml_valid():

    errors = lint_the_xml()
    if errors:
      data = "false"
    else:
      data = "true"
    
    return Response(stream_with_context(data), mimetype='text/plain')

