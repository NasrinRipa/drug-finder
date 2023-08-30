import torch
import gradio as gr
from joblib import load
from sklearn.multioutput import MultiOutputClassifier
import pandas as pd
import numpy as np
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import joblib

# Load the saved model
model_file = "Medicine_Library8.joblib"
loaded_model = load(model_file)

def predict_drug(text_input):
    
    # Perform prediction using the loaded model
    prediction = loaded_model.predict([text_input])[0]
    drug_name = prediction[0]
    drug_uses = prediction[1]
    drug_dosage = prediction[2]
    drug_side_effects = prediction[3]

    output_text = f"DRUG NAME:\n {drug_name}, \n\nDRUG USES:\n {drug_uses}, \n\nDRUG DOSAGE:\n {drug_dosage}, \n\nSIDE EFFECTS:\n {drug_side_effects}\n"
    return output_text

# Create the interface
iface = gr.Interface(
    fn=predict_drug,
    inputs=gr.inputs.Textbox(lines=3, label="Tell me something about the drug you are looking for: "),
    outputs=gr.outputs.Textbox(label="\n\nPredicted drug details\n\n")
)

# Launch the interface
iface.launch()
