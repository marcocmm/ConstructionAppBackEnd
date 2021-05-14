from flask import Blueprint, request, make_response, jsonify
from bson.json_util import dumps
from  werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
import db
from app import app

HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED       = 201
HTTP_SUCCESS_DELETED       = 204
HTTP_SERVER_ERROR          = 500
HTTP_NOT_FOUND             = 404
HTTP_BAD_REQUEST           = 400

bp_login = Blueprint('login', __name__, url_prefix='/login')

@bp_login.route('/', methods=['POST'])
def login():
    message = ""
    res_data = {}
    code = 500
    status = "fail"
    try:
        data = request.get_json()
        user = db.db.user.find_one({"nif": f'{data["nif"]}'})

        if user:
            user['_id'] = str(user['_id'])
            if user and check_password_hash(user['senha'], data['senha']):
                time = datetime.utcnow() + timedelta(hours=24)
                token = jwt.encode({
                        "user": {
                            "nif": f"{user['nif']}",
                            "id": f"{user['_id']}",
                        },
                        "exp": time
                    },app.config['JWT_SECRET_KEY'])

                del user['senha']

                message = f"user authenticated"
                code = 200
                status = "successful"
                res_data['token'] = token.decode('utf-8')
                res_data['user'] = user

            else:
                message = "wrong password"
                code = 401
                status = "fail"
        else:
            message = "invalid login details"
            code = 401
            status = "fail"

    except Exception as ex:
        output = {"error": str(ex)}
        return send(output, HTTP_BAD_REQUEST)
    return jsonify({'status': status, "data": res_data, "message":message}), code

def tokenReq(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            try:
                jwt.decode(token, app.config['JWT_SECRET_KEY'])
            except:
                return jsonify({"status": "fail", "message": "unauthorized"}), 401
            return f(*args, **kwargs)
        else:
            return jsonify({"status": "fail", "message": "unauthorized"}), 401
    return decorated

def send(data, status_code):
    return make_response(dumps(data), status_code)