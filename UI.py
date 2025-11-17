import streamlit as st
import zipfile
import random
from io import BytesIO
from PIL import Image

ALL_IMAGES_ZIP = "image_files/all_images.zip"
DISTORTED_IMAGES_ZIP = "image_files/distorted_images.zip"
CLEAN_IMAGES_ZIP = "image_files/clean_images.zip"

st.title("Image Viewer")

def get_random_image_from_zip(zip_path: str) -> Image.Image:
    """Returns a randomly selected image from the given .zip file."""
    with zipfile.ZipFile(zip_path, 'r') as z:
        # Get list of image files (avoid folders or text files)
        files = [f for f in z.namelist() if f.lower().endswith((".png", ".jpg", ".jpeg"))]

        if not files:
            st.error(f"No images found in {zip_path}")
            return None

        random_file = random.choice(files)
        with z.open(random_file) as img_file:
            img = Image.open(BytesIO(img_file.read())).convert("RGB")
            return img

col1, col2, col3 = st.columns(3)
selected = None

with col1:
    if st.button("Random All Image"):
        img = get_random_image_from_zip(ALL_IMAGES_ZIP)
        if img:
            image_placeholder.image(img, use_container_width=True)

with col2:
    if st.button("Random Distorted Image"):
        img = get_random_image_from_zip(DISTORTED_IMAGES_ZIP)
        if img:
            image_placeholder.image(img, use_container_width=True)

with col3:
    if st.button("Random Clean Image"):
        img = get_random_image_from_zip(CLEAN_IMAGES_ZIP)
        if img:
            image_placeholder.image(img, use_container_width=True)

image_placeholder = st.empty()
if selected:
    img = get_random_image_from_zip(selected)
    if img:
        image_placeholder.image(img, use_container_width=True)
