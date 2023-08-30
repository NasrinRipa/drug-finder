from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def predict_drug(input_text):
    response = requests.post("https://nasrin2023ripa-medicine-library.hf.space/run/predict", json={
        "data": [
            input_text
        ]
    }).json()
    
    predicted_text = response["data"][0]  # Get the first item from the 'data' list
    return predicted_text

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        input_text = request.form['text']
        output_text = predict_drug(input_text)
        return render_template("results.html", input_text=input_text, output_text=output_text)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)



