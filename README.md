# Canvas API Postman

Script to extract the current API documentation from Canvas and generate an importable Postman collection.

`python3 canvas-api-postman.py`

Outputs an 'output.json' file that is used for import into Postman

In Postman choose Import -> Import File -> navigate to this folder

Once in Postman you'll need to set ```domian``` and ```user_token``` variables.

For example:

```domain: yourschool.instructure.com```

```user_token: 12345~abcdefg...789```
