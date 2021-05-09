from flask import Blueprint, current_app, session, request
import db

HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED       = 201
HTTP_SUCCESS_DELETED       = 204
HTTP_SERVER_ERROR          = 500
HTTP_NOT_FOUND             = 404
HTTP_BAD_REQUEST           = 400

bp_equipment = Blueprint('equipment', __name__, url_prefix='/equipment')

@bp_equipment.route('/equipment', methods=['POST']) 
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
        db.db.equipment_collection.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_equipment.route("/all", methods=['GET'])
def getAllEquipments():
    cursor = db.db.equipment_collection.find({})
    return dumps(list(cursor))

@bp_equipment.route('/<_id>', methods=['PUT'])
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
        query = { "_id": int(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.equipment_collection.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_equipment.route('/<_id>', methods=['GET'])
def getEquipment(_id):
    try:
        lista_users = list(db.db.equipment_collection.find({"_id": int(_id)}))
        return send({"result": lista_users}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_equipment.route('/<_id>', methods=['DELETE'])
def deleteEquipment(_id):
    try:
        cursor = db.db.equipment_collection.find_one_and_delete({"_id": int(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)