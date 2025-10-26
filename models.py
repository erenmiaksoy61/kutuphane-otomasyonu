from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Kullanici(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    kullanici_adi = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    sifre = db.Column(db.String(200), nullable=False)

class Kitap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    yazar = db.Column(db.String(100), nullable=False)
    yayin_yili = db.Column(db.Integer)
    durum = db.Column(db.String(20), default="Mevcut")
