from flask import Flask, render_template, request
from wtforms import Form, TextField, validators

from sqlalchemy import Column, Integer, String, create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker, Session

app = Flask(__name__)

# Database_Config is a file which has one value on each line, 
#+ in order:
#+ * dbDriver (e.g. mysql+pmysql)
#+ * dbHostname (e.g. localhost)
#+ * dbUsername (e.g. magicaldbuser)
#+ * dbPassword (e.g. supersneakypassword)
#+ * dbName (e.g. scouting)
database_config = '/etc/scouting-database-config.txt'

#insert db classes here

Base = declarative_base()

class sesh(object):
    def __init__(self):
        self.set_Connection()

    def set_Connection(self):
        with open(database_config, "r") as f:
            self.dbDriver = f.readline().strip()
            self.dbHostname = f.readline().strip()
            self.dbUsername = f.readline().strip()
            self.dbPassword = f.readline().strip()
            self.dbName = f.readline().strip()

    def create_Session(self):
        Session = sessionmaker()
        self.sess = Session.configure(bind=self.engine)
        self.sess = Session()

    def create_Engine(self):
        self.set_Connection()
        self.engine = create_engine(self.dbDriver + "://" + self.dbUsername + ":" + self.dbPassword + "@" + self.dbHostname + "/" + self.dbName)

class Choice(Base):
    """
    CREATE TABLE IF NOT EXISTS scout.choices (
        id INTEGER NOT NULL AUTO_INCREMENT,
        choice VARCHAR(1024),
        PRIMARY KEY (id)
    );
    """
    __tablename__ = 'choices'
    
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    choice = Column(String(1024))
    
    def __repr__(self):
        return "<Choice(id='%d', choice='%s')>" % (
            self.id, self.choice)

class Question(Base):
    """
    CREATE TABLE IF NOT EXISTS scout.questions (
        id INTEGER NOT NULL AUTO_INCREMENT,
        question VARCHAR(1024),
        PRIMARY KEY (id)
    );
    """
    __tablename__ = 'questions'
    
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    question = Column(String(1024))

    def __repr__(self):
        return "<Question(id='%d', question='%s')>" % (
            self.id, self.question)

class Team(Base):
    """
    CREATE TABLE IF NOT EXISTS scout.teams (
        id INTEGER NOT NULL AUTO_INCREMENT,
        teamnumber VARCHAR(8),
        question INTEGER REFERENCES scout.questions,
        choice INTEGER REFERENCES scout.choices,
        PRIMARY KEY (id)
    );
    """
    __tablename__ = 'teams'
    
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    teamnumber = Columns(String)
    question_id = ForeignKey('questions.id')
    choice_id = ForeignKey('choices.id')
    
    question = relationship('Question', foreign_keys='Team.question_id')
    choice = relationship('Choice', foreign_keys='Team.choice_id')
    
    def __repr__(self):
        return "<Team(id='%d', teamnumber='%s', question='%s', choice='%s')>" % (
            self.id, self.teamnumber, self.question, self.choice)

#creating a session
dbsession = sesh()
dbsession.create_Engine()
dbsession.create_Session()
teams = dbsession.sess.query(information).all()

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
    app.run(debug=True,host="0.0.0.0")
