from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# Modify the predict_drug function to return a dictionary with 'uses', 'dosage', 'side_effects' keys
def predict_drug(input_text):
    response = requests.post("https://nasrin2023ripa-medicine-library.hf.space/run/predict", json={
        "data": [
            input_text
        ]
    }).json()
    
    # Assuming the response contains 'data' key with the required information
    predicted_text = response["data"][0]  # Get the first item from the 'data' list
    
    return {
        "uses": predicted_text.get('uses', ''),
        "dosage": predicted_text.get('dosage', ''),
        "side_effects": predicted_text.get('side_effects', '')
    }


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




