from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    serialize_rules = ('-signups.camper', )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    signups = db.relationship("Signup", backref = "camper")

    # @validates('name')
    # def validate_name(self, key, name):
    #     names = db.session.query(Camper.name).all()
    #     if not name:
    #         raise ValueError("Camper must have a Name")
    #     return names
    
    # @validates('age')
    # def validate_age(self, key, age):
    #     if age > 8:
    #         return ValueError("Camper must be at least 8 years old to participate")
    #     elif age < 18:
    #         return ValueError("Camper must be under 18 to participate")
    #     return age
    
    def __repr__(self):
        return f'<Camper id={self.id}, name={self.name}, age={self.age}>'

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    serialize_rules = ('-signups.activity', )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    signups = db.relationship("Signup", backref = "activity")

    def __repr__(self):
        return f'<Activity id={self.id}, name={self.name}, difficulty={self.difficulty}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    serialize_rules = ('-activity.signups', '-camper.signups', )

    id = db.Column(db.Integer, primary_key=True)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    @validates
    def validate_time(self, key, time):
        meet_time = db.session.query(Signup.time).all()
        if time < 0 or time > 23:
            raise ValueError("Activity must take place between 0 and 2300")
        return meet_time

    def __repr__(self):
        return f'<Signup id={self.id}, camper_id={self.camper_id}, activity_id={self.activity_id}, time={self.time} >'