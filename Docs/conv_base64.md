

# Base64 Rider
This part gives you the possibility to encode your data to base64.

## /conv/base64/form
This page offers a comfortable HTML form to enter data and convert it. Use the button on the left side of the lower input field to copy the encoded data to the clipboard.
 

## /conv/base64/json
This interface accepts POST requests and awaits the data in the field _data_. Response is given as JSON structure (content type application/json) with the main key "encoded" as response which contains the encoded data. 

Examples:
```
$ curl -X POST -d 'data2lint=---'  http://192.168.99.101/lint/yaml/json
{"valid": true}

$ curl -X POST -d 'data=hello'  http://192.168.99.101/conv/base64/json
{
    "encoded": "aGVsbG8="
}
```

## /conv/base64/text
This interface accepts POST requests and awaits the data in the field _data_. Response is simply the encoded data as content type text/plain.

Example:
```
$ curl -X POST -d 'data2lint=---'  http://192.168.99.101/conv/base64/text
aGVsbG8=
```
