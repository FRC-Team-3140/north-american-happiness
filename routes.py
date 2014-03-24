from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, TextField, validators

from sqlalchemy import Column, Integer, String, create_engine, desc, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker, Session
from sqlalchemy.orm import relationship

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
        return self.sess

    def create_Engine(self):
        self.set_Connection()
        self.engine = create_engine(self.dbDriver + "://" + self.dbUsername + ":" + self.dbPassword + "@" + self.dbHostname + "/" + self.dbName)
        return self.engine

class Choice(Base):
    """
    CREATE TABLE IF NOT EXISTS scout.choices (
        id INTEGER NOT NULL AUTO_INCREMENT,
        choice VARCHAR(1024),
        parent_question INTEGER REFERENCES scout.questions,
        PRIMARY KEY (id)
    );
    """
    __tablename__ = 'choices'
    
    id = Column(Integer, primary_key=True)
    choice = Column(String(1024))
    parent_question_id = Column(Integer, ForeignKey('questions.id'))
    parent_question = relationship("Question", backref="choices")

    def __repr__(self):
        return "<Choice(id='%d', choice='%s', parent_question_id=%r)>" % (
            self.id, self.choice, self.parent_question_id)

class Question(Base):
    """
    CREATE TABLE IF NOT EXISTS scout.questions (
        id INTEGER NOT NULL AUTO_INCREMENT,
        question VARCHAR(1024),
        lock INTEGER,
        PRIMARY KEY (id)
    );
    """
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True)
    question = Column(String(1024))
    lock = Column(Integer)

    def __repr__(self):
        return "<Question(id='%d', question='%s', lock=%s)>" % (
            self.id, self.question, "True" if self.lock == 1 else "False")

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
    
    id = Column(Integer, primary_key=True)
    teamnumber = Column(String(8))
    question_id = Column(ForeignKey(Question.id))
    choice_id = Column(ForeignKey(Choice.id))
    
    question = relationship('Question', foreign_keys='Team.question_id')
    choice = relationship('Choice', foreign_keys='Team.choice_id')
    
    def __repr__(self):
        return "<Team(id='%d', teamnumber='%s', question='%s', choice='%s')>" % (
            self.id, self.teamnumber, self.question.question, self.choice.choice)

#creating a session
dbsession = sesh()
engine = dbsession.create_Engine()
session = dbsession.create_Session()
#teams = dbsession.sess.query(information).all()

class information(Form):
    #barebones example of how to use wtf forms
    team_number = TextField('Team Number', [validators.Length(min=2,max=4)])


@app.route('/update/<team_number>', methods=['GET', 'POST'])
def update(team_number):
    # data expected to be like:
    # ( (1, "LabVIEW"), (3, "_2"), ... )
    data = zip(map(int, request.args.getlist('qid')), request.args.getlist('a'))
    for (qid, answer) in data:
        if answer[0] == "_":
            answer = int(answer[1:])
        else:
            choice = Choice(choice=answer, parent_question_id=qid)
            session.add(choice)
            session.commit()
            answer = choice.id
        team = Team(teamnumber=team_number, question_id=qid, choice_id=answer)
        session.add(team)
        session.commit()
    return redirect(url_for('front_page', disp_success=team_number))
    

@app.route('/')
def front_page():
    data = {
        "questions": session.query(Question).all(),
        "disp_success": request.args.get('disp_success', default=None),
        }
    #data = information(request.form)
    """ 
    SELECT questions.question_id, 
    FROM questions
    INNER JOIN 
    """
    #data = "Sadness"
    #using validators with the forms
    #if data.validate():
    return render_template('index.html', title='Home', data=data)


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
