import math

from flask import Flask,render_template,request
from src.pipeline.prediction_pipeline import CustomData,PredictPipeline


application=Flask(__name__)

PREPROCESSOR_PATH = "artifacts/preprocessing.pkl"
MODEL_PATH = "artifacts/model.pkl"

NUMERIC_RANGES = {
    "carat": (0.20, 5.01),
    "depth": (43.0, 79.0),
    "table": (43.0, 95.0),
    "x": (0.01, 10.74),
    "y": (0.01, 58.9),
    "z": (0.01, 8.06),
}

CATEGORICAL_VALUES = {
    "cut": {"Fair", "Good", "Very Good", "Premium", "Ideal"},
    "color": {"D", "E", "F", "G", "H", "I", "J"},
    "clarity": {"IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2"},
}


def _parse_and_validate_form(form_data):
    validated_data = {}

    for field, (minimum, maximum) in NUMERIC_RANGES.items():
        raw_value = form_data.get(field)
        try:
            value = float(raw_value)
        except (TypeError, ValueError):
            return None, f"{field.title()} must be a valid number."

        if not math.isfinite(value):
            return None, f"{field.title()} must be a finite number."

        if value < minimum or value > maximum:
            return None, (
                f"{field.title()} must be between {minimum} and {maximum} "
                "to stay within the model's supported range."
            )

        validated_data[field] = value

    for field, allowed_values in CATEGORICAL_VALUES.items():
        value = form_data.get(field)
        if value not in allowed_values:
            return None, f"Please select a valid {field} value."

        validated_data[field] = value

    return validated_data, None

@application.route('/')
def home_page():
    return render_template("index.html")

@application.route("/predict",methods=["GET","POST"])

def predict_datapoint():
    if request.method == "GET":
        return render_template("form.html")
    
    else:
        validated_data, error = _parse_and_validate_form(request.form)
        if error:
            return render_template("form.html", error=error), 400

        data=CustomData(
            carat=validated_data['carat'],
            depth=validated_data['depth'],
            table=validated_data['table'],
            x=validated_data['x'],
            y=validated_data['y'],
            z=validated_data['z'],
            cut=validated_data['cut'],
            color=validated_data['color'],
            clarity=validated_data['clarity']
        )
        final_new_data=data.get_data_as_dataframe()
        predict_pipeline=PredictPipeline()
        pred=predict_pipeline.predict(final_new_data)
        
        result=round(max(0.0, float(pred[0])),2)
        
        return render_template("results.html",final_result=result)
    
    
if __name__ == '__main__' :
        application.run(host="0.0.0.0", debug = True)
