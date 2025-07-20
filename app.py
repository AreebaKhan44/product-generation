# app.py
import streamlit as st
from PIL import Image
import base64
import openai

# Load API key from secrets.toml
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="🛍️ Product SEO Generator", layout="centered")
st.title("🛍️ AI Product Content Generator")

uploaded_image = st.file_uploader("📤 Upload your product image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Product", use_column_width=True)

    if st.button("✨ Generate SEO Content"):
        with st.spinner("⏳ Generating SEO content..."):

            # Convert image to base64
            b64_image = base64.b64encode(uploaded_image.getvalue()).decode()

            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You're a professional SEO content writer."},
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": (
                                        "This is a product image. Based on the image, write:\n"
                                        "1. SEO Title\n"
                                        "2. Product Description (150 words)\n"
                                        "3. Meta Description\n"
                                        "4. 5 SEO Keywords\n"
                                        "5. Instagram Caption"
                                    )
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{b64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=0.7,
                    max_tokens=700
                )

                content = response.choices[0].message.content
                st.markdown("### ✅ SEO Content Generated")
                st.write(content)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
