from dns.message import QUESTION
from dns.resolver import reset_default_resolver
from flask import Blueprint, current_app, session, request, make_response
from bson.objectid import ObjectId
from controllers.login import tokenReq
from bson.json_util import dumps
import db

HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED       = 201
HTTP_SUCCESS_DELETED       = 204
HTTP_SERVER_ERROR          = 500
HTTP_NOT_FOUND             = 404
HTTP_BAD_REQUEST           = 400

bp_service = Blueprint('service', __name__, url_prefix='/service')


@bp_service.route("/all", methods=['GET'])
@tokenReq
def getAllServices():
    cursor = db.db.service.find({})
    return dumps(list(cursor))

@bp_service.route('', methods=['GET'])
@tokenReq
def getService():
    try:
        _id = request.args.get('service_id')
        service = list(db.db.service.find({"_id": ObjectId(_id)}))
        return send({"result": service}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_service.route('/service', methods=['POST'])
@tokenReq
def insertService():
    try:
        request_data = request.get_json() 
        new_store = {
        'nome': request_data['nome'],
        'tipo': request_data['tipo'],
        'valor': request_data['valor'],
        'fornecedor_id': request_data['fornecedor_id'],
        'dataCompra': request_data['dataCompra'],
        'notaFiscalURL': request_data['notaFiscalURL'],
        }
        db.db.service.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)



@bp_service.route('', methods=['PUT'])
@tokenReq
def updateService():
    try:
        request_data = request.get_json() 
        update_store = {
        'nome': request_data['nome'],
        'tipo': request_data['tipo'],
        'valor': request_data['valor'],
        'fornecedor_id': request_data['fornecedor_id'],
        'dataCompra': request_data['dataCompra'],
        'notaFiscalURL': request_data['notaFiscalURL'],
        }
        query = { "_id": ObjectId(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.service.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_service.route('', methods=['DELETE'])
@tokenReq
def deleteService():
    try:
        _id = request.args.get('service_id')
        cursor = db.db.service.find_one_and_delete({"_id": ObjectId(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

def send(data, status_code):
    return make_response(dumps(data), status_code)
