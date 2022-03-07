#################
#### imports ####
#################

from os.path import join, isfile

from flask import Flask, render_template, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy


################
#### config ####
################

heroku_database_path = os.getenv('DATABASE_URL', None)

app = Flask(__name__, instance_relative_config=True)
if isfile(join('instance', 'flask_full.cfg')):
    app.config.from_pyfile('flask_full.cfg')
else:
    app.config.from_pyfile('flask.cfg')


if heroku_database_path:
    app.config["SQLALCHEMY_DATABASE_URI"] = heroku_database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


####################
#### blueprints ####
####################

from project.stocks.views import stocks_blueprint
from project.stocks_api.views import stocks_api_blueprint

# register the blueprints
app.register_blueprint(stocks_blueprint)
app.register_blueprint(stocks_api_blueprint)

############################
#### custom error pages ####
############################

from project.models import ValidationError

@app.errorhandler(ValidationError)
def bad_request(e):
    response = jsonify({'status': 400, 'error': 'bad request',
                        'message': e.args[0]})
    response.status_code = 400
    return response


@app.errorhandler(400)
def page_not_found(e):
    return make_response(jsonify({'error': 'Not found'}), 400)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


@app.errorhandler(410)
def page_not_found(e):
    return render_template('410.html'), 410

