import streamlit as st
from PIL import Image
import base64
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ✅ Initialize OpenAI client
client = OpenAI(api_key=api_key)

st.title("🛍️ AI Product Content Generator")

uploaded_image = st.file_uploader("Upload your product image", type=["jpg", "png", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Product", use_column_width=True)

    if st.button("Generate SEO Content"):
        with st.spinner("Thinking..."):
            # Convert image to base64
            buffered = uploaded_image.getvalue()
            b64_image = base64.b64encode(buffered).decode()

            # GPT-4o Vision Prompt
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a professional SEO content writer."},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Based on this product image, write:\n1. SEO title\n2. Product description (150 words)\n3. Meta description\n4. 5 SEO keywords\n5. Instagram caption"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                        ]
                    }
                ],
                temperature=0.7,
                max_tokens=700
            )

            content = response.choices[0].message.content
            st.markdown("### 📄 Generated SEO Content")
            st.write(content)
