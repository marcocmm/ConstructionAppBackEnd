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

bp_construction = Blueprint('construction', __name__, url_prefix='/construction')

@bp_construction.route("/all", methods=['GET'])
@tokenReq
def getAllConstruction():
    cursor = db.db.construction.find({})
    return dumps(list(cursor))

@bp_construction.route('/<_id>', methods=['GET'])
@tokenReq
def getConstruction(_id):
    try:
        construction = list(db.db.construction.find({"_id": int(_id)}))
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
        'colaboradores_id': request_data['colaboradores_id'],
        'consumiveis_id': request_data['consumiveis_id'],
        'equipamentos_id': request_data['equipamentos_id'],
        'cliente_id': request_data['cliente_id'],
        'materiais_id': request_data['materiais_id'],
        'servicos_id': request_data['servicos_id']
        }
        db.db.construction.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)



@bp_construction.route('/<_id>', methods=['PUT'])
@tokenReq
def updateConstruction():
    try:
        request_data = request.get_json() 
        update_store = {
        'nome': request_data['nome'],
        'imageURL': request_data['imageURL'],
        'colaboradores_id': request_data['colaboradores_id'],
        'consumiveis_id': request_data['consumiveis_id'],
        'equipamentos_id': request_data['equipamentos_id'],
        'cliente_id': request_data['cliente_id'],
        'materiais_id': request_data['materiais_id'],
        'servicos_id': request_data['servicos_id']
        }
        query = { "_id": int(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.construction.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_construction.route('/<_id>', methods=['DELETE'])
@tokenReq
def deleteConstruction(_id):
    try:
        cursor = db.db.construction.find_one_and_delete({"_id": int(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

def send(data, status_code):
    return make_response(dumps(data), status_code)