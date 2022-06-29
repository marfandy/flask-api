from functools import wraps
from textwrap import wrap
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api

import jwt
import datetime

from configs import SECRET_KEY
from models.employee import Employee


class TokenBearer():
    def __init__(self) -> None:
        pass

    def create_token(self, data: Employee) -> dict:

        token = jwt.encode(
            {
                "username": data.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }, SECRET_KEY, algorithm="HS256"
        )
        data.login = True
        data.save()
        return jsonify({
            "token": token
        })

    def token_required(self, f):
        @wraps(f)
        def decorator(*args, **kwargs):
            token = request.headers.get('token')

            if not token:
                return make_response(jsonify({"message": "Invalid Token!"}), 400)
            try:
                decode = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                user = Employee.query.filter(
                    Employee.username == decode.get('username')).first()
                if not user.login:
                    return make_response(jsonify({"message": "Already logout!"}), 404)
            except:
                return make_response(jsonify({"message": "Invalid Token!"}), 404)

            return f(*args, **kwargs)

        return decorator

    def decode_jwt(self):
        token = request.headers.get('token')
        output = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        return output.get('username')
