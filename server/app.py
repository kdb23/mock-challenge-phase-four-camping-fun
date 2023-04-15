from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response = make_response(
            {
                "message": "Hello Campers!"
            },
            200
        )
        return response

api.add_resource(Home, '/')

class Campers(Resource):
    def get(self):
        kids = Camper.query.all()
        kid_list = []
        for c in kids:
            c_dict = {
                'id': c.id,
                'name': c.name,
                'age': c.age,
            }
            kid_list.append(c_dict)

        return make_response(jsonify(kid_list), 200)

    def post(self):
        data = request.get_json()
        try:
            new_kid = Camper (
                name=data['name'],
                age=data['age']
            )
        except ValueError:
            return make_response({'error': 'validation error'}, 422)
        db.session.add(new_kid)
        db.session.commit()

        return make_response(new_kid.to_dict(), 201)

    
api.add_resource(Campers, '/campers' )

class CamperById(Resource):


      def get(self, id):
        camper = Camper.query.filter_by(id = id).first()
        if  not camper:
            return make_response({'message': 'Camper Not Found'}, 404)
        
        camper_dict = {
            'id': camper.id,
            'name': camper.name,
            'age': camper.age,
            'activites': []
        }
        for events in camper.activities:
            activity ={
            'id':events.id,
            'name':events.name,
            'difficulty':events.difficulty
            }
            camper_dict['activites'].append(activity)

        return make_response(jsonify(camper_dict), 200)

    


api.add_resource(CamperById, '/campers/<int:id>')


class Activities(Resource):
    def get(self):
        fun = Activity.query.all()
        fun_list = []
        for f in fun:
            f_dict = {
                'id': f.id,
                'name': f.name,
                'difficulty': f.difficulty, 
            }
            fun_list.append(f_dict)

        return make_response(jsonify(fun_list), 200)

api.add_resource(Activities, '/activities')

class ActivitiesById(Resource):
    def get(self, id):
        play_time = Activity.query.filter_by(id = id).to_dict()
        return make_response(jsonify(play_time), 200)
    
    def delete(self, id):
        doomed_activity = Activity.query.filter_by(id = id).first()
        if not doomed_activity:
            return make_response({'error': 'Activity Not Found'}, 404)
        else:
            db.session.delete(doomed_activity)
            db.session.commit()

            return make_response({'message': ''}, 200)

api.add_resource(ActivitiesById, '/activities/<int:id>')

class Signups(Resource):

    def get(self):
        fun_times = [fun.to_dict() for fun in Signup.query.all()]
        return make_response(jsonify(fun_times), 200)

    def post(self):
        data = request.get_json()
        try:
            new_signup = Signup (
                time=data['time'],
                camper_id=data['camper_id'],
                activity_id=data['activity_id']
            )
        except ValueError:
            return make_response({'errors': 'validation error'}, 400)
        db.session.add(new_signup)
        db.session.commit()

        return make_response(new_signup.activity.to_dict(), 201)
    

api.add_resource(Signups, '/signups')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

