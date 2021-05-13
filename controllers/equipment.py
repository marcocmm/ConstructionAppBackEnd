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

bp_equipment = Blueprint('equipment', __name__, url_prefix='/equipment')

@bp_equipment.route('/equipment', methods=['POST'])
@tokenReq 
def insertEquipment():
    try:
        request_data = request.get_json() 
        new_store = {
        'nome': request_data['nome'],
        'tipo': request_data['tipo'],
        'fornecedor_id': request_data['fornecedor_id'],
        'dataCompra': request_data['dataCompra'],
        'valor': request_data['valor'],
        'notaFiscalURL': request_data['notaFiscalURL']
        }
        db.db.equipment.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_equipment.route("/all", methods=['GET'])
@tokenReq
def getAllEquipments():
    cursor = db.db.equipment.find({})
    return dumps(list(cursor))

@bp_equipment.route('', methods=['PUT'])
@tokenReq
def updateEquipment():
    try:
        request_data = request.get_json() 
        update_store = {
        'nome': request_data['nome'],
        'tipo': request_data['tipo'],
        'fornecedor_id': request_data['fornecedor_id'],
        'dataCompra': request_data['dataCompra'],
        'valor': request_data['valor'],
        'notaFiscalURL': request_data['notaFiscalURL']
        }
        query = { "_id": ObjectId(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.equipment.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_equipment.route('', methods=['GET'])
@tokenReq
def getEquipment():
    try:
        _id = request.args.get('equipment_id')
        equipment = list(db.db.equipment.find({"_id": ObjectId(_id)}))
        return send({"result": equipment}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_equipment.route('', methods=['DELETE'])
@tokenReq
def deleteEquipment():
    try:
        _id = request.args.get('equipment_id')
        cursor = db.db.equipment.find_one_and_delete({"_id": ObjectId(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

def send(data, status_code):
    return make_response(dumps(data), status_code)