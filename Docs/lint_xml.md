
# For a Few XML More
These are the interfaces to lint a XML. Choose one according to your needs. Error details reporting is not implemented _yet_.

## /lint/xml/form
This page offers a comfortable HTML form to enter a XML and lint it. On clicking the button, the app checks the XML and gives feedback as an unordered list (to be implemented), or, in best case, tells you that the XML is valid.
 
### /lint/xml/csv
This interface accepts POST requests and awaits the XML in the field _data_. Response is given as CSV list (content type text/csv), which remains empty (zero lines) if the XML is valid.

Example:
```
$ curl -X POST -d 'data=<xml>no</yaml>'  http://192.168.99.101/lint/xml/csv
0,0,error reporting not yet implemented
```

## /lint/xml/json
This interface accepts POST requests and awaits the XML in the field _data_. Response is given as JSON structure (content type application/json) with the main key "valid" as response which is giving you the result _true_ or _false_. If there's errors, you'll find an array with line number, column and description (to be implemented). 

Examples:
```
$ curl -X POST -d 'data=<xml></xml>'  http://192.168.99.101/lint/xml/json
{"valid": true}

$ curl -X POST -d 'data=<this>is no<xml>'  http://192.168.99.101/lint/xml/json
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

## /lint/xml/valid
This interface accepts POST requests and awaits the XML in the field _data_. Response is given as simply _true_ or _false_ (content type text/plain).

Example:
```
$ curl -X POST -d 'data=<this>is no<xml>'  http://192.168.99.101/lint/xml/valid
false
```
