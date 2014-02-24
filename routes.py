from flask import Flask, render_template, request
from wtforms import Form, TextField, validators

from sqlalchemy import Column, Integer, String, create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker, Session

app = Flask(__name__)

#insert db classes here

Base = declarative_base()

class sesh(object):
    def __init__(self):
        self.set_Connection()

    def set_Connection(self):
        self.dbDriver   = 'mysql+pymysql'
        self.dbHostname = ''#REDACTED!
        self.dbUsername = 'root'
        self.dbPassword = ''#REDACTED!
        self.dbName     = ''#REDACTED!

    def create_Session(self):
        Session = sessionmaker()
        self.sess = Session.configure(bind=self.engine)
        self.sess = Session()

    def create_Engine(self):
        self.set_Connection()
        self.engine = create_engine(self.dbDriver + "://" + self.dbUsername + ":" + self.dbPassword + "@" + self.dbHostname + "/" + self.dbName)


#template class for sqlalchemy
'''class class_name(Base):
    __tablename__ = 'data'

    team_number = Column(Integer, primary_key=True)
    name     = Column(String)
    city     = Column(String)
    info     = Column(String)
    other    = Column(String)
    leader   = Column(String)
    date     = Column(DATE)

    def __init__(self, team_number, name, city, info, other, leader, date)
        team_number = Column(Integer, primary_key=True)
        name     = Column(String)
        city     = Column(String)
        info     = Column(String)
        other    = Column(String)
        leader   = Column(String)
        date     = Column(DATE)

    def __repr__(self):
        return '<class_name("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (self.team_number, self.name, self.city, self.info, self.other, self.leader, self.date)
'''

#creating a session
'''
dbsession = sesh()
dbsession.create_Engine()
dbsession.create_Session()
teams = dbsession.sess.query(information).all()
'''

class information(Form):
    #barebones example of how to use wtf forms
    team_number = TextField('Team Number', [validators.Length(min=2,max=4)])


@app.route('/')
def front_page():
    data = information(request.form)
    #using validators with the forms
    #if data.validate():
    return render_template('index.html', title='Home', data=data)


if __name__ == '__main__':
    app.run(debug=True)
