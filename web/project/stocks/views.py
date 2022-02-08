# project/stocks/views.py

#################
#### imports ####
#################

from flask import render_template, Blueprint, request, redirect, url_for, flash
from project import db, app
from project.models import Stock, Tweet
from random import random
from ..streamer import TwitterStreamer


################
#### config ####
################

stocks_blueprint = Blueprint('stocks', __name__)


##########################
#### helper functions ####
##########################

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')



################
#### routes ####
################

@stocks_blueprint.route('/')
def home_page():
    public_stocks = Stock.query.filter((Stock.logo != "")).limit(4)
    return render_template('home_page.html', public_stocks=public_stocks)

@stocks_blueprint.route('/stocks/<sector>')
def all_stocks(sector='All'):
    if sector in ['Technology', 'Communication Services', 'Consumer Cyclical', 'Healthcare', 'Energy', 'Financial Services']:
        my_stocks = Stock.query.filter((Stock.sector == sector))
        return render_template('all_stocks.html', all_stocks=my_stocks, sector=sector)
    elif sector == 'All':
        my_stocks = Stock.query.filter((Stock.sector != ""))
        return render_template('all_stocks.html', all_stocks=my_stocks, sector=sector)
    else:
        flash('ERROR! Invalid sector selected.', 'error')

    return redirect(url_for('stocks.home_page'))


@stocks_blueprint.route('/stock/<stock_id>')
def stock_details(stock_id):
    stock = Stock.query.filter_by(id=stock_id).first_or_404()
    tweets = Tweet.query.filter((Tweet.stock_name == stock.name)).order_by(Tweet.id.desc()).limit(10)
    return render_template('stock_detail.html', stock=stock, tweets=tweets)

