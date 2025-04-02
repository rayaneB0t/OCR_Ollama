# source venv/bin/activate

import streamlit as st
import os
from PIL import Image
import io
import base64
import requests
import json
from pathlib import Path

# Ensure assets directory exists
Path("./assets").mkdir(parents=True, exist_ok=True)

# Function to call Groq API directly (avoiding the groq package)
def call_groq_api(image_base64, model, prompt):
    api_key = os.environ.get("GROQ_API_KEY", "")
    
    if not api_key:
        return None, "Error: GROQ_API_KEY environment variable is not set."
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "temperature": 0.1,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"], None
    except Exception as e:
        return None, f"Error calling Groq API: {str(e)}"


# Page configuration
st.set_page_config(
    page_title="llama-3.2-90b-vision-preview",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Add clear button to top right
col1, col2 = st.columns([6,1])
with col1:
    st.markdown("""
    # <img src="data:image/png;base64,{}" width="50" style="vertical-align: -12px;"> llama-3.2-90b-vision-preview
    """.format(base64.b64encode(open("img/llama.png", "rb").read()).decode()), unsafe_allow_html=True)

with col2:
    if st.button("Clear 🗑️"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        st.rerun()

st.markdown('Extract structured text from images using Vision Models!', unsafe_allow_html=True)
st.markdown("---")

# Move upload controls to sidebar
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    
    # Model selection
    st.subheader("Model Settings")
    model = st.selectbox(
        "Select Vision Model",
        ["llama-3.2-11b-vision-preview", "llama-3.2-90b-vision-preview"],
        index=0
    )
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        
        if st.button("Extract Text 🔍", type="primary"):
            with st.spinner("Processing image..."):
                try:
                    # Convert image for API
                    buffered = io.BytesIO()
                    image.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                    
                    # Prepare the prompt
                    prompt = """Analyze the text in the provided image. Extract all readable content
                             and present it in a structured Markdown format that is clear, concise, 
                             and well-organized. Ensure proper formatting (e.g., headings, lists, or
                             code blocks) as necessary to represent the content effectively."""
                    
                    # Call the API
                    result, error = call_groq_api(img_str, model, prompt)
                    
                    if error:
                        st.error(error)
                    else:
                        st.session_state['ocr_result'] = result
                        
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")

# Main content area for results
if 'ocr_result' in st.session_state:
    st.markdown(st.session_state['ocr_result'])
else:
    st.info("Upload an image and click 'Extract Text' to see the results here.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Vision Models via Groq API | NovamAI - Rayane Tarkany")