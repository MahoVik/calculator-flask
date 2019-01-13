import json
import flask
from flask import request
from calculator_flask.rpn import rpn


app = flask.Flask(__name__)


@app.route("/calc", methods=["POST"])
def calculate():
    d = request.get_json(force=True)
    if not isinstance(d, dict):
        # Throw an error
        # "The given data is not a dict!"
        resp = app.response_class(
            response=json.dumps({
                'status': 400,
                'message': "The given data is not a dict!"
            }),
            status=400,
        )
        return resp

    if 'expression' not in d:
        # Throw an error
        # "The key 'expression' required'
        resp = app.response_class(
            response=json.dumps({
                'status': 400,
                'message': "The key 'expression' required"
            }),
            status=400,
        )
        return resp

    expression = d.get('expression')
    if not isinstance(expression, str):
        resp = app.response_class(
            response=json.dumps({
                'status': 400,
                'message': "The given data is not a string!"
            }),
            status=400,
        )
        return resp
    try:
        res = rpn.evaluate(expression)
    except Exception as e:
        resp = app.response_class(
            response=json.dumps({
                'status': 400,
                'message': str(e)
            }),
            status=400,
        )
        return resp

    return json.dumps({"result": res})


@app.route('/', methods=['POST', 'GET'])
def calc_form():
    error = None
    res = None
    if request.method == 'POST':
        d = request.form
        mathexpression = d.get('expression')
        if not isinstance(mathexpression, str):
            error = "The given data is not a string!"
        elif len(mathexpression) == 0:
            error = "The given data is empty!"
        try:
            res = rpn.evaluate(mathexpression)
        except Exception as e:
            error = str(e)

    # следущий код выполняется при методе запроса GET
    # или при признании полномочий недействительными

    return flask.render_template('index.html', error=error, res=res)


def main():
    app.run(host='0.0.0.0.', port=8000)


if __name__ == "__main__":
    main()
