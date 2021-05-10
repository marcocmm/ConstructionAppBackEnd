from flask import Blueprint, current_app, session, request
import db

HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED       = 201
HTTP_SUCCESS_DELETED       = 204
HTTP_SERVER_ERROR          = 500
HTTP_NOT_FOUND             = 404
HTTP_BAD_REQUEST           = 400

bp_provider = Blueprint('provider', __name__, url_prefix='/provider')

@bp_provider.route("/all", methods=['GET'])
def getAllProviders():
    cursor = db.db.provider.find({})
    return dumps(list(cursor))

@bp_provider.route('/<_id>', methods=['GET'])
def getProvider(_id):
    try:
        provider = list(db.db.provider.find({"_id": int(_id)}))
        return send({"result": provider}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_provider.route('/provider', methods=['POST']) 
def insertProvider():
    try:
        request_data = request.get_json() 
        new_store = {
        'nome': request_data['nome'],
        'telefone': request_data['telefone'],
        'endereco': request_data['endereco'],
        'nipc': request_data['nipc'],
        'contratoURL': request_data['contratoURL'],
        }
        db.db.provider.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)



@bp_provider.route('/<_id>', methods=['PUT'])
def updateProvider():
    try:
        request_data = request.get_json() 
        update_store = {
        'nome': request_data['nome'],
        'telefone': request_data['telefone'],
        'endereco': request_data['endereco'],
        'nipc': request_data['nipc'],
        'contratoURL': request_data['contratoURL'],
        }
        query = { "_id": int(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.provider.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_provider.route('/<_id>', methods=['DELETE'])
def deleteProvider(_id):
    try:
        cursor = db.db.provider.find_one_and_delete({"_id": int(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)