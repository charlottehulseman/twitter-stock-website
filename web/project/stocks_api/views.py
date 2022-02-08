# project/stocks_api/views.py

#################
#### imports ####
#################

from flask import Blueprint, request, jsonify, g
from project import db
from project.models import Stock
from .decorators import etag


################
#### config ####
################

stocks_api_blueprint = Blueprint('stocks_api', __name__)


########################
#### error handlers ####
########################

@stocks_api_blueprint.errorhandler(404)
def api_error(e):
    response = jsonify({'status': 404, 'error': 'not found (API!)', 'message': 'invalid resource URI'})
    response.status_code = 404
    return response


@stocks_api_blueprint.errorhandler(405)
def api_error(e):
    response = jsonify({'status': 405, 'error': 'method not supported (API!)', 'message': 'method is not supported'})
    response.status_code = 405
    return response


@stocks_api_blueprint.errorhandler(500)
def api_error(e):
    response = jsonify({'status': 500, 'error': 'internal server error (API!)', 'message': 'internal server error occurred'})
    response.status_code = 500
    return response

################
#### routes ####
################

@stocks_api_blueprint.before_request
#@auth_token.login_required
def before_request():
    """All routes in this blueprint require authentication."""
    pass


@stocks_api_blueprint.after_request
@etag
def after_request(rv):
    """Generate an ETag header for all routes in this blueprint."""
    return rv


@stocks_api_blueprint.route('/api/v1/stocks', methods=['GET'])
def api_1_get_all_stocks():
    return jsonify({'stocks': [stock.get_url() for stock in Stock.query.all()]})

@stocks_api_blueprint.route('/api/v1/stocks/<int:stock_id>', methods=['GET'])
def api_1_get_stock(stock_id):
    return jsonify(Stock.query.get_or_404(stock_id).export_data())

@stocks_api_blueprint.route('/api/v1/stocks', methods=['POST'])
def api_1_create_stock():
    new_stock = Stock()
    new_stock.import_data(request)
    db.session.add(new_stock)
    db.session.commit()
    return jsonify({}), 201, {'Location': new_stock.get_url()}


@stocks_api_blueprint.route('/api/v1/stocks/<int:stock_id>', methods=['PUT'])
def api_1_update_stock(stock_id):
    stock = Stock.query.get_or_404(stock_id)
    stock.import_data(request)
    db.session.add(stock)
    db.session.commit()
    return jsonify({'result': 'True'})


@stocks_api_blueprint.route('/api/v1/stocks/<int:stock_id>', methods=['DELETE'])
def api_1_delete_stock(stock_id):
    stock = Stock.query.get_or_404(stock_id)
    db.session.delete(stock)
    db.session.commit()
    return jsonify({'result': True})
