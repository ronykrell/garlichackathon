from flask import Flask, request, redirect, url_for
from flask_restful import Resource, Api
from joblib import load
import numpy as np
import pandas as pd
import sklearn
from flask_cors import CORS, cross_origin

# Upload folder
UPLOAD_FOLDER = 'img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

api = Api(app)

latest_pred = 0
latest_actual = 0


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_prediction(json_row):
    # json_row = json.loads(feature_row)
    features_array = json_row['feature_row'][:10]
    actual_movement = json_row['feature_row'][-1]
    np_arr = np.array(features_array).reshape(1,-1)
    prediction = model.predict(np_arr)[0]
    print(prediction)
    print("Ran prediction")
    return {"pred": prediction, "actual": actual_movement}


global global_latest_pred
global global_latest_actual
global global_history
global model

model = load("trained_classifier.joblib")



global_latest_pred = 0
global_latest_actual = 0
global_history = []


class MovementPrediction(Resource):

    def post(self):
        feature_row = request.get_json()
        print(feature_row)
        pred_obj = get_prediction(feature_row)
        global_latest_pred = pred_obj['pred']
        global_latest_actual = pred_obj['actual']
        global_history.append({'pred':  global_latest_pred, 'actual': global_latest_actual})
        print("Added point")
        print(len(global_history))
        return {'success': "True"}

    def get(self):
        ind_json = request.args.get('index')
        print(ind_json)
        ind_num = int(ind_json)
        print(ind_num)
        if len(global_history) < ind_num + 1:
            return {"success": "False"}
        else:
            return global_history[ind_num]


api.add_resource(MovementPrediction, '/predict/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


















