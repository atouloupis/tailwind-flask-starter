from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    name = db.Column(db.String(1000))
    dateOfBirth = db.Column(db.Date())

class Profile(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    profile=b.Column(db.String(100)) #

class Residence(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    number = db.Column(db.Integer)
    street=db.Column(db.String(1000))
    type=db.Column(db.String(100))
    city=db.Column(db.String(1000))
    x=db.Column(db.Integer)
    y=db.Column(db.Integer)
    idBan=db.Column(db.Integer,nullable=False)
    label=db.Column(db.String(1000))
    postcode=db.Column(db.Integer)
    insee=db.Column(db.Integer)
    complement=db.Column(db.String(1000))

class UserProfileResidence(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    userId=db.Column(db.Integer)
    residenceId=db.Column(db.Integer)
    profileId=db.Column(db.Integer)


class Fournisseur(UserMixin, db.Model): 


class FournisseurResidence(UserMixin, db.Model):


class Files(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    storageId=db.Column(db.Integer,unique=True,nullable=False)
    userUpload = db.Column(db.String(100),nullable=False)
    uploadDate = db.Column(db.Date(),nullable=False)
    fileType = db.Column(db.String(100),nullable=False)
    fournisseurId = db.Column(db.Integer)
    residenceId=db.Column(db.Integer,nullable=False)
    metadataFile = db.Column(db.String(1000))