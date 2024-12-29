import torch
import torch.nn as nn
import torch.optim as optim
from torchinfo import summary
from timm import create_model
from torchvision import models

model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 1)
model = model.to("cuda" if torch.cuda.is_available() else "cpu")



# model = create_model("convit_base", pretrained=False, num_classes=1)
# model.head = nn.Linear(model.head.in_features, 1)
# model = model.to("cuda" if torch.cuda.is_available() else "cpu")
device = "cuda" if torch.cuda.is_available() else "cpu"
state_dict = torch.load("resnet18_weights.pth", map_location=torch.device('cpu'))
model.load_state_dict(state_dict)

# Вывод архитектуры модели
print(summary(model, input_size=(1, 3, 224, 224), col_names=["input_size", "output_size", "num_params"]))
