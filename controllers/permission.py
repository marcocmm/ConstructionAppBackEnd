from flask import Blueprint, current_app, session, request
import db

HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED       = 201
HTTP_SUCCESS_DELETED       = 204
HTTP_SERVER_ERROR          = 500
HTTP_NOT_FOUND             = 404
HTTP_BAD_REQUEST           = 400

bp_permission = Blueprint('permission', __name__, url_prefix='/permission')

@bp_permission.route('/permission', methods=['POST'])
def insertPermission():
    try:
        request_data = request.get_json() 
        new_store = {
        'equpamentos': request_data['equpamentos'],
        'material': request_data['material'],
        'consumivel': request_data['consumivel'],
        'clientes': request_data['clientes'],
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
        db.db.permission_collection.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_permission.route('/<_id>', methods=['GET'])
def getPermission(_id):
    try:
        permission = list(db.db.permission_collection.find({"_id": int(_id)}))
        return send({"result": permission}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_permission.route('/<_id>', methods=['DELETE'])
def deletePermission(_id):
    try:
        cursor = db.db.permission_collection.find_one_and_delete({"_id": int(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_permission.route("/all", methods=['GET'])
def getAllUPermissions():
    cursor = db.db.permission_collection.find({})
    return dumps(list(cursor))

@bp_permission.route('/<_id>', methods=['PUT'])
def updatePermission():
    try:
        request_data = request.get_json() 
        update_store = {
        'equpamentos': request_data['equpamentos'],
        'material': request_data['material'],
        'consumivel': request_data['consumivel'],
        'clientes': request_data['clientes'],
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
        query = { "_id": int(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.permission_collection.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)