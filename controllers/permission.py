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

bp_permission = Blueprint('permission', __name__, url_prefix='/permission')

@bp_permission.route('/permission', methods=['POST'])
@tokenReq
def insertPermission():
    try:
        request_data = request.get_json() 
        new_store = {
        'equpamentos': request_data['equpamentos'],
        'material': request_data['material'],
        'consumivel': request_data['consumivel'],
        'customers': request_data['customers'],
        'fornecedores': request_data['fornecedores'],
        'obra': request_data['obra'],
        'presencas': request_data['presencas'],
        'orcamentos': request_data['orcamentos'],
        'faturaMensal': request_data['faturaMensal'],
        'servicos': request_data['servicos'],
        'colaboradores': request_data['colaboradores'],
        'gastosMensais': request_data['gastosMensais'],
        'gastosConsumiveis': request_data['gastosConsumiveis'],
        'recursosHumanos': request_data['recursosHumanos'],
        }
        db.db.permission.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_permission.route('', methods=['GET'])
@tokenReq
def getPermission():
    try:
        _id = request.args.get('permission_id')
        permission = list(db.db.permission.find({"_id": ObjectId(_id)}))
        return send({"result": permission}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_permission.route('', methods=['DELETE'])
@tokenReq
def deletePermission():
    try:
        _id = request.args.get('permission_id')
        cursor = db.db.permission.find_one_and_delete({"_id": ObjectId(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_permission.route("/all", methods=['GET'])
@tokenReq
def getAllUPermissions():
    cursor = db.db.permission.find({})
    return dumps(list(cursor))

@bp_permission.route('', methods=['PUT'])
@tokenReq
def updatePermission():
    try:
        request_data = request.get_json() 
        update_store = {
        'equpamentos': request_data['equpamentos'],
        'material': request_data['material'],
        'consumivel': request_data['consumivel'],
        'customers': request_data['customers'],
        'fornecedores': request_data['fornecedores'],
        'obra': request_data['obra'],
        'presencas': request_data['presencas'],
        'orcamentos': request_data['orcamentos'],
        'faturaMensal': request_data['faturaMensal'],
        'servicos': request_data['servicos'],
        'colaboradores': request_data['colaboradores'],
        'gastosMensais': request_data['gastosMensais'],
        'gastosConsumiveis': request_data['gastosConsumiveis'],
        'recursosHumanos': request_data['recursosHumanos'],
        }
        query = { "_id": ObjectId(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.permission.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


def send(data, status_code):
    return make_response(dumps(data), status_code)