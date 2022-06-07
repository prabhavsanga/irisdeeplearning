
from flask import Flask, render_template, session, redirect, url_for, session
import flask_wtf
from flask_wtf import FlaskForm
from wtforms import TextField,SubmitField
from wtforms.validators import NumberRange
import numpy as np
from tensorflow.keras.models import load_model
import joblib


def return_prediction(model, scaler, sample_json):

    s_len = sample_json[ 'SepalLengthCm']
    s_wid = sample_json[ 'SepalWidthCm']
    p_len = sample_json[ 'PetalLengthCm']
    p_wid = sample_json[ 'PetalWidthCm']

    flower = [[s_len, s_wid, p_len, p_wid]]
    flower = scaler.transform(flower)

    classes = np.array(['setosa' , 'versicolor' , 'virginica'])

    class_ind = model.predict_classes(flower)

    return classes[class_ind][0]

    s_len = sample_json['SepalLengthCm']
    s_wid = sample_json['SepalWidthCm']
    p_len = sample_json['PetalLengthCm']
    p_wid = sample_json['PetalWidthCm']

    lower = [[ s_len , s_wid , p_len , p_wid]]
    flower = scaler.transform(flower)
    classes = np.array(['setosa', 'versicolor', 'virginica'])
    class_ind = model.predict_classes(flower)
    return classes[class_ind][0]


app = Flask(__name__)
# Configure a secret SECRET_KEY
app.config['SECRET_KEY'] = '998877'
# Loading the model and scaler
flower_model = load_model('iris_model.h5')
flower_scaler = joblib.load("iris_scaler.pkl")

# Now create a WTForm Class
class FlowerForm(FlaskForm):
    sep_len = TextField('Sepal Length')
    sep_wid = TextField('Sepal Width')
    pet_len = TextField('Petal Length')
    pet_wid = TextField('Petal Width')
    submit = SubmitField('Analyze')

    @app.route( '/', methods = ['GET' , 'POST'])

    def index(self):
        # Create instance of the form.
        form = FlowerForm()
        # If the form is valid on submission
        if form.validate_on_submit():
            #Grab the data from the input on the form.
            session['sep_len'] = form.sep_len.data
            session['sep_wid'] = form.sep_wid.data
            session['pet_len'] = form.pet_len.data
            session['pet_wid'] = form.pet_wid.data


        return redirect(url_for("prediction"))
        return render_template('home.html', form = form)

        @app.route('/prediction')

        def prediction():
    # Defining content dictionary
            content = {}


        content['sepal_length'] = float(session['sep_len'])
        content['sepal_width'] = float(session['sep_wid'])
        content['petal_length'] = float(session['pet_len'])
        content['petal_width'] = float(session['pet_wid'])

        results = return_prediction(model=flower_model, scaler=flower_scaler, sample_json=content)
        return render_template('prediction.html', results = results)
        if __name__ == '__main__':
         app.run(debug=True)
