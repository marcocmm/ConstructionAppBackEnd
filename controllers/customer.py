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

bp_customer = Blueprint('customer', __name__, url_prefix='/customer')

@bp_customer.route("/all", methods=['GET'])
@tokenReq
def getAllcustomers():
    cursor = db.db.customer.find({})
    return dumps(list(cursor))

@bp_customer.route("/allbyconstruction", methods=['GET'])
@tokenReq
def getAllCustomersByConstruction():
    _id = request.args.get('obra_id')
    customer = list(db.db.customer.find({"obra_id": ObjectId(_id)}))
    return send({"result": customer}, HTTP_SUCCESS_GET_OR_UPDATE)

@bp_customer.route('', methods=['GET'])
@tokenReq
def getcustomer():
    try:
        _id = request.args.get('customer_id')
        customer = list(db.db.customer.find({"_id": ObjectId(_id)}))
        return send({"result": customer}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_customer.route('/customer', methods=['POST'])
@tokenReq 
def insertcustomer():
    try:
        request_data = request.get_json() 
        new_store = {
        'nome': request_data['nome'],
        'telefone': request_data['telefone'],
        'nipcnif': request_data['nipcnif'],
        'obra_id': ObjectId(request_data['obra_id']),
        } 
        db.db.customer.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)



@bp_customer.route('', methods=['PUT'])
@tokenReq
def updatecustomer():
    try:
        request_data = request.get_json() 
        update_store = {
        'nome': request_data['nome'],
        'telefone': request_data['telefone'],
        'nipcnif': request_data['nipcnif'],
        }
        query = { "_id": ObjectId(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.customer.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_customer.route('', methods=['DELETE'])
@tokenReq
def deletecustomer():
    try:
        _id = request.args.get('customer_id')
        cursor = db.db.customer.find_one_and_delete({"_id": ObjectId(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

def send(data, status_code):
    return make_response(dumps(data), status_code)