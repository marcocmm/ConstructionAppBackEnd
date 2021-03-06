from flask import Blueprint, current_app, session, request, make_response
from controllers.login import tokenReq
from bson.objectid import ObjectId
from bson.json_util import dumps
import db

HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED       = 201
HTTP_SUCCESS_DELETED       = 204
HTTP_SERVER_ERROR          = 500
HTTP_NOT_FOUND             = 404
HTTP_BAD_REQUEST           = 400

bp_construction = Blueprint('construction', __name__, url_prefix='/construction')

@bp_construction.route("/all", methods=['GET'])
@tokenReq
def getAllConstruction():
    cursor = db.db.construction.find({})
    return dumps(list(cursor))

@bp_construction.route('', methods=['GET'])
@tokenReq
def getConstruction():
    try:
        _id = request.args.get('obra_id')
        construction = list(db.db.construction.find({"_id": ObjectId(_id)}))
        return send({"result": construction}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_construction.route('/construction', methods=['POST'])
@tokenReq 
def insertConstruction():
    try:
        request_data = request.get_json() 
        new_store = {
        'nome': request_data['nome'],
        'imageURL': request_data['imageURL'],
        'dataInicio': request_data['dataInicio']
        }
        db.db.construction.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)



@bp_construction.route('', methods=['PUT'])
@tokenReq
def updateConstruction():
    try:
        request_data = request.get_json() 
        update_store = {
        'nome': request_data['nome'],
        'imageURL': request_data['imageURL'],
        'dataInicio': request_data['dataInicio']
        }
        query = { "_id": ObjectId(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.construction.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_construction.route('', methods=['DELETE'])
@tokenReq
def deleteConstruction():
    try:
        _id = request.args.get('obra_id')
        cursor = db.db.construction.find_one_and_delete({"_id": ObjectId(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

def send(data, status_code):
    return make_response(dumps(data), status_code)