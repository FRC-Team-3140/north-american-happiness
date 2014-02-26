from routes import *

for question in ["Programming language", "Primary mechanism", "Secondary mechanism",
                 "Tertiary mechanism"]:
    session.add(Question(question=question))


