from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    gender = db.Column(db.String(120), unique=True, nullable=False)
    dob = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    picture = db.Column(db.String(120), unique=True, nullable=False)
    parent_id = db.Column(db.Integer, ForeignKey('person.id'))
    parents = db.relationship('Parents', remote_side=[id],
        backref=db.backref('Children', lazy=True))
    child_id = db.Column(db.Integer, ForeignKey('person.id'))
    children = db.relationship('Children', remote_side=[id],
        backref=db.backref('Parents', lazy=True))
    siblings_id = db.Column(db.Integer, ForeignKey('person.id'))
    siblings = db.relationship('Siblings', remote_side=[id],
        backref=db.backref('Siblings', lazy=True))

    def __repr__(self):
        return 'Name: %s' % self.name

    def to_dict(self):
        parents = []
        for parent in self.parents:
            parents.append(parent.to_dict())
        children = []
        for child in self.children:
            children.append(child.to_dict())
        siblings = []
        for sibling in self.siblings:
            siblings.append(sibling.to_dict())
        return {
            "name": self.name,
            "gender": self.gender,
            "dob": self.dob,
            "email": self.email,
            "picture": self.picture,
            "parents": parents,
            "children": children,
            "siblings": siblings
        }