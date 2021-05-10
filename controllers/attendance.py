from flask import Blueprint, current_app, session, request, make_response
from bson.json_util import dumps
from controllers.login import tokenReq
import db

HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED       = 201
HTTP_SUCCESS_DELETED       = 204
HTTP_SERVER_ERROR          = 500
HTTP_NOT_FOUND             = 404
HTTP_BAD_REQUEST           = 400

bp_attendance = Blueprint('attendance', __name__, url_prefix='/attendance')

@bp_attendance.route("/all", methods=['GET'])
@tokenReq
def getAllAttendance():
    cursor = db.db.attendance.find({})
    return dumps(list(cursor))

@bp_attendance.route('/<_id>', methods=['GET'])
@tokenReq
def getAttendance(_id):
    try:
        attendance = list(db.db.attendance.find({"_id": int(_id)}))
        return send({"result": attendance}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_attendance.route('/attendance', methods=['POST'])
@tokenReq 
def insertAttendance():
    try:
        request_data = request.get_json() 
        new_store = {
        'usuario_id': request_data['usuario_id'],
        'obra_id': request_data['obra_id'],
        'dataEntrada': request_data['dataEntrada'],
        'dataSaida': request_data['dataSaida']
        }
        db.db.attendance.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)



@bp_attendance.route('/<_id>', methods=['PUT'])
@tokenReq
def updateAttendance():
    try:
        request_data = request.get_json() 
        update_store = {
        'usuario_id': request_data['usuario_id'],
        'obra_id': request_data['obra_id'],
        'dataEntrada': request_data['dataEntrada'],
        'dataSaida': request_data['dataSaida']
        }
        query = { "_id": int(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.attendance.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_attendance.route('/<_id>', methods=['DELETE'])
@tokenReq
def deleteAttendance(_id):
    try:
        cursor = db.db.attendance.find_one_and_delete({"_id": int(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

def send(data, status_code):
    return make_response(dumps(data), status_code)