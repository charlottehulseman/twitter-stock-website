from project import db
from flask import url_for


# Allowable HTML tags
allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3', 'p']


class ValidationError(ValueError):
    pass

class Stock(db.Model):

    __tablename__ = "stock"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    logo = db.Column(db.String)
    website = db.Column(db.String)
    industry = db.Column(db.String)
    sector = db.Column(db.String)
    size = db.Column(db.String)

    def __init__(self, name, description, logo_link, website_link, industry, sector, size):
        self.name = name
        self.description = description
        self.logo = logo_link
        self.website = website_link
        self.industry = industry
        self.sector = sector
        self.size = size

    def __repr__(self):
        return '<id: {}, name: {}, description: {}>'.format(self.id,
                                                            self.name,
                                                            self.description)

    def get_url(self):
        return url_for('stocks_api.api_1_get_stock', stock_id=self.id, _external=True)

    def export_data(self):
        return {
            'name': self.name,
            'self_url': self.get_url(),
            'Description': self.description,
            'Logo': self.logo,
            'Website': self.website,
            'Industry': self.industry,
            'Sector': self.sector,
            'Size': self.size
        }

class Tweet(db.Model):

    """Tweets about Stocks"""
    __tablename__ = "tweets"

    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String)
    created = db.Column(db.String)
    username = db.Column(db.String)
    text = db.Column(db.String)

    def __init__(self, stock_name, created, username,text):
        self.stock_name = stock_name
        self.created_at = created
        self.username = username
        self.text = text

    def __repr__(self):
        return '<id: {}, stock_name: {}>'.format(self.id, self.stock_name)

    def export_data(self):
        return {
            "stock_name": self.stock_name,
            "created_at": self.created_at,
            "username": self.username,
            "text": self.text
        }
