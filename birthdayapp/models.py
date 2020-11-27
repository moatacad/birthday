from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from birthdayapp import db


class Guest(db.Model):
    __tablename__='guest'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    pwd = db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(100))
    guest_fullname=db.Column(db.String(100))
    guest_state=db.Column(db.Integer(),db.ForeignKey('state.state_id'))
    date_registered=db.Column(db.DateTime(), default=datetime.utcnow)
    guest_pix=db.Column(db.String(100))
    #relationship
    trx=db.relationship('Transaction',backref='guest', uselist=False)

class Transaction(db.Model): 
    id = db.Column(db.Integer(), primary_key=True)
    trxamt = db.Column(db.Float())
    trxref = db.Column(db.String(100), nullable=False)
    trxstatus=db.Column(db.Enum('Pending','Paid','Failed'))
    trxothers=db.Column(db.String(100))
    trxdate=db.Column(db.DateTime(), default=datetime.utcnow)
    guest_id=db.Column(db.Integer(),db.ForeignKey('guest.id'))
  


class State(db.Model):
    __tablename__='state'
    state_id=db.Column(db.Integer(), primary_key=True)
    state_name=db.Column(db.String(100))
    #set up relationship
    guests=db.relationship('Guest',backref='statedetails')

class Gift(db.Model):
    gift_id=db.Column(db.Integer(), primary_key=True)
    gift_name=db.Column(db.String(100))
    gift_guestid=db.Column(db.Integer())

class StateTable(db.Model):
    __tablename__='tbl_state'
    state_id=db.Column(db.Integer(), primary_key=True)
    state_name=db.Column(db.String(100)) 

class Lga(db.Model):
    __tablename__='lga'
    lga_id=db.Column(db.Integer(), primary_key=True)
    state_id=db.Column(db.Integer())
    lga_name=db.Column(db.String(100))

class Topics(db.Model):
    topicid=db.Column(db.Integer(), primary_key=True)
    topicname=db.Column(db.String(100))
    topicdescription=db.Column(db.String(100))

