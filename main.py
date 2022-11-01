from prediction_validation_insertion import pred_validation
from PredictionModel import prediction
from flask import Flask, render_template, request
import flask_monitoringdashboard as dashboard
from flask_cors import CORS, cross_origin
import os
from flask import Response

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)

dashboard.bind(app)
CORS(app)



@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route('/predict',methods = ['POST'])

def predictRouteClient():
    try:
        if request.method == 'POST':
            path = request.form['filepath']

            data = pred_validation(path)

            data.PredValidation()

            tr = prediction(path)
            tr.PredModel()

            if os.path.exists('Prediction_Output_File'):
                return Response("Prediction File created at %s!!!" % path)


            
    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)

if __name__ == "__main__":
    app.run(debug=True)