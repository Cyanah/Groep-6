import torch
import torch.nn as nn
import numpy as np
from PIL import Image
import torchvision.transforms as transforms

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_path = "python_files/model.pkl"
model = torch.load(model_path, map_location=device)

model.eval()
model.to(device)

transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.ToTensor()
])

def preprocess(img: Image.Image) -> torch.Tensor:
  tensor = transform(img).unsqueeze(0)
  return tensor.to(device)

def run_autoencoder(img: Image.Image):
  x = preprocess(img)
  with torch.no_grad():
    reconstructed = model(x)
  x_np = x.cpu().numpy()
  recon_np = reconstructed.cpu().numpy()
  mse = np.mean((x_np - recon_np) ** 2)
  return float(mse)
