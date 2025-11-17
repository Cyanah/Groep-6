import streamlit as st
import zipfile
import random
from io import BytesIO
from PIL import Image

ALL_IMAGES_ZIP = "image_files/all_images.zip"
DISTORTED_IMAGES_ZIP = "image_files/distorted_images.zip"
CLEAN_IMAGES_ZIP = "image_files/clean_images.zip"

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

col1, col2, col3 = st.columns(3)
selected = None

with col1:
    if st.button("Random All Image"):
        selected = ALL_IMAGES_ZIP

with col2:
    if st.button("Random Distorted Image"):
        selected = DISTORTED_IMAGES_ZIP

with col3:
    if st.button("Random Clean Image"):
        selected = CLEAN_IMAGES_ZIP

image_placeholder = st.empty()
if selected:
    img = get_random_image_from_zip(selected)
    if img:
        image_placeholder.image(img, use_container_width=True)
