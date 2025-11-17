import streamlit as st
import zipfile
import random
from io import BytesIO
from PIL import Image
import requests
import base64

ALL_IMAGES_ZIP = "image_files/all_images.zip"
DISTORTED_IMAGES_ZIP = "image_files/distorted_images.zip"
CLEAN_IMAGES_ZIP = "image_files/clean_images.zip"

API_URL = "http://127.0.0.1:8000/predict"

st.title("Image Viewer")

st.write("In deze site zijn er plaatjes van cijfers ikgeladen. Echter zijn er een aantal vertekende plaatjes aanwezig. Deze worden geprobeerd geïdentificeert te worden en dan het midden te blurren. Echte resultaten worden minder geblurred gemaakt.")

def get_random_image_from_zip(zip_path: str) -> Image.Image:
    with zipfile.ZipFile(zip_path, 'r') as z:
        files = [f for f in z.namelist()
                 if f.lower().endswith((".png", ".jpg", ".jpeg"))]

        if not files:
            st.error(f"No images found in {zip_path}")
            return None

        random_file = random.choice(files)
        with z.open(random_file) as img_file:
            return Image.open(BytesIO(img_file.read())).convert("RGB")

if "current_image" not in st.session_state:
    st.session_state.current_image = None

col1, col2, col3 = st.columns(3)
selected = None

with col1:
    if st.button("Random All Image"):
        st.session_state.current_image = get_random_image_from_zip(ALL_IMAGES_ZIP)

with col2:
    if st.button("Random Distorted Image"):
        st.session_state.current_image = get_random_image_from_zip(DISTORTED_IMAGES_ZIP)

with col3:
    if st.button("Random Clean Image"):
        st.session_state.current_image = get_random_image_from_zip(CLEAN_IMAGES_ZIP)

image_placeholder = st.empty()
if selected:
    img = get_random_image_from_zip(selected)
    if img:
        image_placeholder.image(img, use_container_width=True)


if st.session_state.current_image:
    st.image(st.session_state.current_image, caption="Selected Image", use_container_width=True)

    # Prediction button
    if st.button("Run Model Prediction"):
        # Convert image to bytes
        img_bytes = BytesIO()
        st.session_state.current_image.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        # Send to FastAPI
        files = {"file": ("input.png", img_bytes, "image/png")}
        response = requests.post(API_URL, files=files)

        if response.status_code == 200:
            data = response.json()

            st.success("Prediction complete!")
            st.write(f"**MSE:** {data['prediction']}")

        else:
            st.error("API request failed.")
