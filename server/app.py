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
    
api.add_resource(Campers, '/campers' )

class CamperById(Resource):
    def get(self, id):
        camper = Camper.query.filter_by(id = id).first()
        if camper:
            camper_dict ={
                'id': camper.id,
                'name': camper.name,
                'age': camper.age,
                'activities': []
            }
            activities = Activity.query.filter_by(id = id).all()
            for a in activities:
                fun_time = {
                    'id': a.id,
                    'name': a.name,
                    'difficulty': a.difficulty
                }
                camper_dict['activities'].append(fun_time)

            return make_response(jsonify(camper_dict), 200)
        else:
            return make_response({'message': 'Camper Not Found'}, 404)
    


api.add_resource(CamperById, '/campers/<int:id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)
