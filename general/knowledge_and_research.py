import streamlit as st
from PIL import Image
import os
import io

image_path = r"C:\Users\ADMIN\Project\Heart\heart-malfunction-classification\general\newspaper_1.png"

def load_image(image_file):
    try:
        img = Image.open(image_file)
        return img
    except FileNotFoundError:
        st.error(f"Image not found: {image_file}")
        return None

def create_half_image(image):
    width, height = image.size
    half_height = height // 2
    half_img = image.crop((0, 0, width, half_height))
    return half_img

def image_to_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def create_newspaper_card(title, content, image_file):
    with st.container():
        st.subheader(title)
        
        image = load_image(image_file)
        if image:
            half_img = create_half_image(image)
            half_img_bytes = image_to_bytes(half_img)
            full_img_bytes = image_to_bytes(image)
        else:
            st.write("Image not available")
            return

        expanded = st.expander("Read article", expanded=False)
        
        with expanded:
            col1, col2 = st.columns([3, 7])
            
            with col1:
                st.image(full_img_bytes, use_column_width=True)
            
            with col2:
                st.write(content)
        
        if not expanded.expanded:
            col1, col2 = st.columns([3, 7])
            
            with col1:
                st.image(half_img_bytes, use_column_width=True)
            
            with col2:
                st.write(content[:100] + "...")
        
        st.markdown("---")  # Add a horizontal line to separate articles

st.title("News on Cardiovascular Health")

newspapers = [
    {
        "title": "New Study Reveals Link Between Diet and Heart Health",
        "content": "A groundbreaking study published in the Journal of Cardiology has uncovered a strong correlation between dietary habits and cardiovascular health. The research, conducted over a period of 10 years, involved more than 100,000 participants from diverse backgrounds.\n\nKey findings include:\n\n1. People who consume a Mediterranean-style diet have a 30% lower risk of heart disease.\n2. High consumption of processed foods is associated with a 25% increase in cardiovascular events.\n3. Regular intake of omega-3 fatty acids can reduce the risk of arrhythmias by up to 20%.\n\nDr. Emily Johnson, the lead researcher, emphasizes the importance of these findings: 'Our study provides concrete evidence that what we eat has a direct impact on our heart health. It's not just about avoiding harmful foods, but also about incorporating heart-healthy options into our daily diet.'\n\nThe study recommends increasing the consumption of fruits, vegetables, whole grains, and lean proteins while reducing the intake of saturated fats, added sugars, and excessive salt.\n\nThis research underscores the critical role of nutrition in preventing and managing cardiovascular diseases, which remain the leading cause of death globally. Health experts are calling for more public education on the importance of a heart-healthy diet and lifestyle changes to combat the rising tide of heart disease.",
        "image": image_path
    },
    # Add more newspaper articles here
]

for paper in newspapers:
    create_newspaper_card(paper["title"], paper["content"], paper["image"])
