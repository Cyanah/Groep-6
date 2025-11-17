from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from python_files.inference import run_autoencoder
from PIL import Image
import io

app = FastAPI()

# Allow Streamlit frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Receive an image file and return autoencoder result."""
    
    # Read uploaded file
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")

    # Run the autoencoder prediction
    result = run_autoencoder(img)

    return {
        "prediction": result,
        "status": "success"
    }
