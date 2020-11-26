
# The Good, the Bad and the JSON
These are the interfaces to lint a JSON. Choose one according to your needs. The basic python json library stops at the first error so you always get a list/array with just the next error as answer.

## /lint/json/form
This page offers a comfortable HTML form to enter a JSON and lint it. On clicking the button, the app checks the JSON and gives feedback as an unordered list, or, in best case, tells you that the JSON ist valid.
 
## /lint/json/csv
This interface accepts POST requests and awaits the JSON in the field _data_. Response is given as CSV list (content type text/csv), which remains empty (zero lines) if the JSON is valid.

Example:
```
$ curl -X POST -d 'data={ "this": is no valid json }'  http://192.168.99.101/lint/json/csv
1,11,Expecting value
```

### /lint/json/json
This interface accepts POST requests and awaits the JSON in the field _data_. Response is given as JSON structure (content type application/json) with the main key "valid" as response giving you the result _true_ or _false_. If there's errors, you'll find an array with line number, column and description. 

Examples:
```
$ curl -X POST -d 'data={}'  http://192.168.99.101/lint/json/json
{"valid": true}

$ curl -X POST -d 'data={ "this": is no valid json }'  http://192.168.99.101/lint/json/json
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

## /lint/json/valid
This interface accepts POST requests and awaits the JSON in the field _data_. Response is given as simply _true_ or _false_ (content type text/plain).

Example:
```
$ curl -X POST -d 'data={ "this": is no valid json }'  http://192.168.99.101/lint/json/csv
false
```

