from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        input_text = request.form['text']
        output = predict_drug(input_text)[0]
        confidence_list = output['confidences']

        #drug_name = prediction[0]
        #drug_uses = prediction[1]
        #drug_dosage = prediction[2]
        #drug_side_effects = prediction[3]
        #output_text = f"DRUG NAME:\n {drug_name}, \n\nDRUG USES:\n {drug_uses}, \n\nDRUG DOSAGE:\n {drug_dosage}, \n\nSIDE EFFECTS:\n {drug_side_effects}\n"
    #return output_text

        labels = [elem['label'] for elem in confidence_list if elem['confidence'] >= 0.5 ]
        label_text = ""
        for idx, label in enumerate(labels):
            label_text = label_text + label
            if idx != len(labels)-1: label_text = label_text + ", "
        return render_template("results.html", input_text=input_text, output_text=label_text)
    else:
        return render_template("index.html")

def predict_drug(input_text):
    response = requests.post("https://nasrin2023ripa-medicine-library.hf.space//run/predict", json={
        "data": [
            input_text
        ]
    }).json()
    data = response["data"]
    return data

if __name__ == "__main__":
    app.run(debug=True)



