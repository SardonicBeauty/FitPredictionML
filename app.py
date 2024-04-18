from flask import Flask, request, render_template, jsonify
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

# Define the fit_i_mapping dictionary
fit_i_mapping = {
    'fit': 0,
    'small': 1,
    'large': 2
}

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/predict', methods=['POST', "GET"])
def predict_datapoint(): 
    if request.method == "GET": 
        return render_template("main.html")
    else: 
        data = CustomData(
            weight=int(request.form.get('weight')),
            category=str(request.form.get('category')),
            size=int(request.form.get("size")), 
            age=int(request.form.get("age")), 
            height=float(request.form.get("height")),
            body_type=request.form.get("body_type"), 
        )
        new_data = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(new_data)

        # Convert prediction to string label using fit_i_mapping
        prediction_label = next(key for key, value in fit_i_mapping.items() if value == int(pred[0]))

        return render_template("result.html", final_result=prediction_label)

if __name__ == "__main__": 
    app.run(host="0.0.0.0", debug=True)
