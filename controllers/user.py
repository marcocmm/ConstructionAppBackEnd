from flask import Blueprint, current_app, session, request
import db

HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED       = 201
HTTP_SUCCESS_DELETED       = 204
HTTP_SERVER_ERROR          = 500
HTTP_NOT_FOUND             = 404
HTTP_BAD_REQUEST           = 400

bp_user = Blueprint('user', __name__, url_prefix='/user')

@bp_user.route("/all", methods=['GET'])
def getAllUsers():
    cursor = db.db.users.find({})
    return dumps(list(cursor))

@bp_user.route('/<_id>', methods=['GET'])
def getUser(_id):
    try:
        lista_users = list(db.db.users.find({"_id": int(_id)}))
        return send({"result": lista_users}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_user.route('/users', methods=['POST']) 
def insertUser():
    try:
        request_data = request.get_json() 
        new_store = {
        'nome': request_data['nome'],
        'senha': request_data['senha'],
        'telefone': request_data['telefone'],
        'tipo_usuario_id': request_data['tipo_usuario_id'],
        'nif': request_data['nif'],
        }
        db.db.users.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)



@bp_user.route('/<_id>', methods=['PUT'])
def updateUser():
    try:
        request_data = request.get_json() 
        update_store = {
        'nome': request_data['nome'],
        'senha': request_data['senha'],
        'telefone': request_data['telefone'],
        'tipo_usuario_id': request_data['tipo_usuario_id'],
        'nif': request_data['nif'],
        }
        query = { "_id": int(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.users.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_user.route('/<_id>', methods=['DELETE'])
def deleteUser(_id):
    try:
        cursor = db.db.users.find_one_and_delete({"_id": int(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)