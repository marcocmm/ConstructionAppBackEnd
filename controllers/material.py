from flask import Blueprint, current_app, session, request, make_response
from controllers.login import tokenReq
from bson.json_util import dumps
import db

HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED       = 201
HTTP_SUCCESS_DELETED       = 204
HTTP_SERVER_ERROR          = 500
HTTP_NOT_FOUND             = 404
HTTP_BAD_REQUEST           = 400

bp_material = Blueprint('material', __name__, url_prefix='/material')

@bp_material.route("/all", methods=['GET'])
@tokenReq
def getAllMaterials():
    cursor = db.db.material.find({})
    return dumps(list(cursor))

@bp_material.route('/<_id>', methods=['GET'])
@tokenReq
def getMaterial(_id):
    try:
        material = list(db.db.material.find({"_id": int(_id)}))
        return send({"result": material}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_material.route('/material', methods=['POST'])
@tokenReq 
def insertMaterial():
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
        db.db.material.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_material.route('/<_id>', methods=['PUT'])
def updateMaterial():
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
        query = { "_id": int(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.material.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_material.route('/<_id>', methods=['DELETE'])
@tokenReq
def deleteMaterial(_id):
    try:
        cursor = db.db.material.find_one_and_delete({"_id": int(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

def send(data, status_code):
    return make_response(dumps(data), status_code)