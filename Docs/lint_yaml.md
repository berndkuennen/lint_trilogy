

# A Fistful of YAML
These are the interfaces to lint a YAML. Choose one according to your needs.

## /lint/yaml/form
This page offers a comfortable HTML form to enter a YAML and lint it. On clicking the button, the app checks the YAML and gives feedback as an unordered list, or, in best case, tells you that the YAML ist valid.
 
### /lint/yaml/csv
This interface accepts POST requests and awaits the YAML in the field _data_. Response is given as CSV list (content type text/csv), which remains empty (zero lines) if the YAML is valid.

Example:
```
$ curl -X POST -d 'data=xxx '  http://192.168.99.101/lint/yaml/csv
1,1,missing document start "---"
1,4,trailing spaces
```

## /lint/yaml/json
This interface accepts POST requests and awaits the YAML in the field _data_. Response is given as JSON structure (content type application/json) with the man key "value" as response which is telling with a _true_ or _false_ if the YAMl is valid. If there's errors, you'll find an array with line number, column and description. 

Examples:
```
$ curl -X POST -d 'data=---'  http://192.168.99.101/lint/yaml/json
{"valid": true}

$ curl -X POST -d 'data=xxx '  http://192.168.99.101/lint/yaml/json
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

## /lint/yaml/valid
This interface accepts POST requests and awaits the YAML in the field _data_. Response is given as simply _true_ or _false_ (content type text/plain).

Example:
```
$ curl -X POST -d 'data=---'  http://192.168.99.101/lint/yaml/valid
true
```
