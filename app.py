from flask import Flask, jsonify, request, make_response
from pymongo import MongoClient
from bson.json_util import dumps
import db
app = Flask(__name__)

HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED       = 201
HTTP_SUCCESS_DELETED       = 204
HTTP_SERVER_ERROR          = 500
HTTP_NOT_FOUND             = 404
HTTP_BAD_REQUEST           = 400

#Error Handler 404
@app.errorhandler(404)
def not_found_error(error):
    return send({'error': 'Not found error'}, HTTP_SERVER_ERROR)

#Error Handler 500
@app.errorhandler(500)
def internal_server_error(error):
    return send({'error': 'Internal server error'}, HTTP_SERVER_ERROR)

#Exception
@app.errorhandler(Exception)
def unhandled_exception(error):
    try:
        return send({'error': str(error)}, HTTP_SERVER_ERROR)
    except:
        return send({'error': "Unknown error"}, HTTP_SERVER_ERROR)

def send(data, status_code):
    return make_response(dumps(data), status_code)

if __name__ == '__main__':
    from controllers.attendance import bp_attendance
    app.register_blueprint(bp_attendance)

    from controllers.client import bp_client
    app.register_blueprint(bp_client)

    from controllers.construction import bp_construction
    app.register_blueprint(bp_construction)

    from controllers.consumable import bp_consumable
    app.register_blueprint(bp_consumable)

    from controllers.equipment import bp_equipment
    app.register_blueprint(bp_equipment)

    from controllers.material import bp_material
    app.register_blueprint(bp_material)

    from controllers.permission import bp_permission
    app.register_blueprint(bp_permission)

    from controllers.provider import bp_provider
    app.register_blueprint(bp_provider)

    from controllers.service import bp_service
    app.register_blueprint(bp_service)

    from controllers.user import bp_user
    app.register_blueprint(bp_user)

    from controllers.user_type import bp_user_type
    app.register_blueprint(bp_user_type)
    
    app.run(port=8000)