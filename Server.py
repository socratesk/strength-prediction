# import Flask class from the flask module
from flask import Flask, render_template, request

import pickle
import pandas

# Create Flask object to run
app = Flask(__name__)

global concrete_strength_predictor_model
print ("Loading model...")
concrete_strength_predictor_file = open('model/concrete_xgb_deloyable_model_ver_1_0.sav', 'rb')
concrete_strength_predictor_model = pickle.load(concrete_strength_predictor_file)
concrete_strength_predictor_file.close()

global concrete_days_dict
print ("Loading dictionary...")
concrete_days_file = open('model/concrete_days_ver_1_0.dict', 'rb')
concrete_days_dict = pickle.load(concrete_days_file)
concrete_days_file.close()
	
@app.route('/')
@app.route('/index')
def home():
    return "Hi, Welcome to Flask!!"

	
# Render Concrete mixture input page
@app.route('/input')
def input():
    return render_template('input.html')

	
# This function will be called when the input page is submitted
@app.route('/predict', methods=["POST"])
def predict():

    # Enter into this snippet of the code only if the method is POST.
	if request.method == "POST":
	
		# Extract each field, cast to float, and pass it as a value to dictionary object
		input_dict = {'cement': float(request.form['cement']),
					  'blast': float(request.form['blast']),
					  'flyash': float(request.form['flyash']),
					  'water': float(request.form['water']),
					  'superplasticizer': float(request.form['superplasticizer']),
					  'coarse_aggregate': float(request.form['coarse_aggregate']),
					  'fine_aggregate': float(request.form['fine_aggregate']),
					  'age': request.form['age']
					 }
					 
		# Construct dataframe out of the dictionary object
		concrete_df = pandas.DataFrame(input_dict, index=[0])
		
		# --------------------------------------------------------------------------------------------------------
		# ****** NOTE: If you have done any feature engineering in the training set, then the same thing has to be 
		# ****** carried-out in user-input as well. This is the right place where you have to carry-out the 
		# ****** feature update on the input dataset.
		
		concrete_df['age'] = concrete_days_dict.get(request.form['age'])
		# --------------------------------------------------------------------------------------------------------
		
		print ("Input values before passing onto model: \n", concrete_df)

		# Pass the dataframe object to loaded ML model and do prediction
		strength_predicted = str(round(concrete_strength_predictor_model.predict(concrete_df)[0], 2))
		print ("Predicted Concrete Strength: ", strength_predicted)

		return render_template('results.html', strength_predicted=strength_predicted)

	
# FOR LOCAL SERVER ONLY	
if __name__ == "__main__":
	print("**Starting Server...")
		
	# Run Server
	app.run()