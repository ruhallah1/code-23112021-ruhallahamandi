import time
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import config
import json

api = Api(prefix=config.API_PREFIX)


class TaskStatusAPI(Resource):
    def get(self, task_id):
        task = celery.AsyncResult(task_id)
        return jsonify(task.result)

class DataProcessingAPI(Resource):
    def post(self):
        task = process_data1.delay()
        return {'task_id': task.id}, 200

    def getcatg(self,bmi):
        self.bmi=bmi
        if(bmi<=18.4):
            res=['Underweight','Malnutrition risk']
        elif((bmi>=18.5) and (bmi<=24.9)):
            res=['Normal Weight','Low risk']
        elif((bmi>=25) and (bmi<=29.9)):
            res=['Overweight','Enhanced risk']
        elif((bmi>=30) and (bmi<=34.9)):
            res=['Moderately Obese','Medium risk']
        elif((bmi>=35) and (bmi<=39.9)):
            res=['Severely Obese','High risk']
        else:
            res=['Very Severely Obese','Very high risk']

        return res

    def get(self):
        json_data = request.get_json(force=True)
        print(json_data)
        total_overweight=0
        resultList = []
        try:
            for j in json_data:
                bmi=float(j['WeightKg'])/((float(j['HeightCm'])/100)**2)
                print(bmi)
                total_overweight +=(0, 1)[(bmi > 25) and (bmi < 29.9)]
                print(self.getcatg(bmi))

                resultList.append([bmi,self.getcatg(bmi)])

            jsonStr = json.dumps(resultList)
            jsonStr = json.loads(jsonStr)
            return json.dumps({'success': True, 'data':jsonStr, 'total_overweight':total_overweight}), 200, {'ContentType': 'application/json'}
        #
        except:
            return json.dumps({'success': False, 'data': ''}), 400, {'ContentType': 'application/json'}


def process_data1():
    time.sleep(60)

# data processing endpoint
api.add_resource(DataProcessingAPI, '/process_data')

# task status endpoint
api.add_resource(TaskStatusAPI, '/tasks/<string:task_id>')