from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import base64
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
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    
    mse, recon_img, guess = run_autoencoder(img)
    
    # Encode reconstruction image to base64
    buffered = BytesIO()
    recon_img.save(buffered, format="PNG")
    recon_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    return JSONResponse({
        "mse": mse,
        "reconstruction": recon_b64,
        "guess": guess
    })
