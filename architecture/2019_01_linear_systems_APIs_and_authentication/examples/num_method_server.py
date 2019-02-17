from functools import wraps
import numpy as np
from flask import Flask, request, Response, jsonify
from numerical_methods import row_interchange, scalar_multiplication, add_scalar_mult
app = Flask(__name__)

creds = {'example_user': 'example_password'}
acceptable_tokens = {'thisshouldbeahashedstringwithhighentropy', }


def check_http_basic_auth(username, password):
    # Hopefully it goes without saying that we would never
    # store these credentials in plain-text in the real world.
    if username is None or password is None:
        return False

    return creds.get(username) == password


def http_login_required(f):
    @wraps(f)
    def required_login_wrapper(*args, **kwargs):
        auth = request.authorization
        if check_http_basic_auth(auth.username, auth.password):
            return f(*args, **kwargs)
        else:
            return Response('Failed auth', 403)

    return required_login_wrapper


def check_api_token(api_token):
    return api_token in acceptable_tokens


def api_token_required(f):
    @wraps(f)
    def required_login_wrapper(*args, **kwargs):
        if check_api_token(request.json['api_token']):
            return f(*args, **kwargs)
        else:
            return Response('Failed token check', 403)
    return required_login_wrapper


def make_array_from_json(js):
    array_as_json = js.get('array')
    try:
        return np.array(array_as_json, dtype=np.float64)
    except Exception:  # Should be catching a more specific error
        return Response('Could not create a NumPy array from request', 400)


@app.route('/row_interchange')
@http_login_required
def basic_auth_row_interchange():
    req_content = request.json
    np_array = make_array_from_json(req_content)
    res = row_interchange(np_array, req_content['index_one'], req_content['index_two'])
    return jsonify(res.tolist())


@app.route('/scalar_multiplication')
@api_token_required
def api_token_scalar_multiplication():
    req_content = request.json
    np_array = make_array_from_json(req_content)
    res = scalar_multiplication(np_array, req_content['mult_index'], req_content['mult_by'])
    return jsonify(res.tolist())


if __name__ == '__main__':
    app.run(debug=True)
