from flask import Flask, render_template, request
import requests

app = Flask(__name__)


def predict_drug(input_text):
    response = requests.post("https://nasrin2023ripa-medicine-library.hf.space/run/predict", json={
        "data": [input_text]
    }).json()
    
    # Check if the expected keys exist in the API response
    if 'uses' in response and 'dosage' in response and 'side_effects' in response:
        drug_details = {
            "uses": response["uses"],
            "dosage": response["dosage"],
            "side_effects": response["side_effects"]
        }
        return drug_details
    else:
        # Handle the case where the expected keys are missing in the API response
        return {"error": "Unexpected response format from the API"}


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        input_text = request.form['text']
        drug_details = predict_drug(input_text)
        return render_template("results.html", input_text=input_text, drug_details=drug_details)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)




