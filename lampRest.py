from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps

import lamp

app = Flask(__name__)
api = Api(app)

class LampOff(Resource):
    def get(self, lampno):
        lamp1 = lamp.Lamp(lampno)
        lamp1.off()
        return "OK"
        #return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID



#api.add_resource(LampOn, '/lampon/<lampno>')
api.add_resource(LampOff, '/lampoff/<lampno>')

if __name__ == '__main__':
     app.run(port='5002')
