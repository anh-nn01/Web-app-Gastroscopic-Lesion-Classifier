"""
Created on Wed Mar, 3, 2021
@author: Nhu Nhat Anh

Run model prediction
"""
import torch
from torchvision import transforms
import numpy as np
from PIL import Image
from Gastric_Models import Gastric_Resnet34

classes = ['Active Gastritis', 'Atrophic Gastritis', 'Chronic Gastritis', 'Intestinal Metaplasia', 'Normal', 'Ulcers']

# Load classification model
model = Gastric_Resnet34(model_dir = "./gastric_resnet34.pth")
model.eval()

def Predict(img):
    # Image preprocessing
    data_transform = transforms.Compose([
        transforms.Resize((224,224), interpolation= Image.NEAREST),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    img = Image.fromarray(img) # Convert to PIL image
    img = data_transform(img)
    img = torch.reshape(img, (1, 3, 224, 224))
    output = model(img).detach().numpy()[0]
    idx = output.argmax()
    
    return classes[idx]