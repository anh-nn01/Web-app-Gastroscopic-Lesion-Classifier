"""
Created on Wed Mar, 3, 2021
@author: Nhu Nhat Anh

Models for gastric classification
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

from torchvision import transforms, models

import numpy as np

"""
Model for Gastroscopy classification - ResNet34 backbone
"""
class Gastric_Resnet34(nn.Module):
    """
    Model architecture
    :param model_dir: path to the trained weights
    """
    def __init__(self, model_dir : str):
        super(Gastric_Resnet34, self).__init__()
        resnet34 = models.resnet34(pretrained=False)
        resnet34.fc = torch.nn.Sequential(
            torch.nn.Linear(512, 256),
            torch.nn.Dropout(p=0.5),
            torch.nn.ReLU(inplace=True),
            torch.nn.Linear(256, 6)
        )
        
        if(torch.cuda.is_available()):
            resnet34.load_state_dict(torch.load("gastric_resnet34.pth"))
        else:
            resnet34.load_state_dict(torch.load("gastric_resnet34.pth", map_location="cpu"))

        self.model = resnet34
        
    def forward(self, img):
        return self.model(img)