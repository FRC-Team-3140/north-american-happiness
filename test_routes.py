from routes import *

#with contextlib.closing(engine.connect()) as con:
#    trans = con.begin()
#    for table in reversed(meta.sorted_tables):
#        con.execute(table.delete())
#    trans.commit()

Base.metadata.create_all(engine)

q1 = Question(question="Programming lanugage?", lock=0)
print q1

(c1, c2, c3) = (Choice(choice="LabVIEW", parent_question_id=q1.id),
                Choice(choice="Java", parent_question_id=q1.id), 
                Choice(choice="C++", parent_question_id=q1.id))
print (c1, c2, c3)

session.add_all([c1, c2, c3, q1])
session.commit()

for q in session.query(Question).all():
    print session.query(Choice).filter(Choice.parent_question_id == q.id).all()

