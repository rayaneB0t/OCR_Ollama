# Llama 3.2 Vision OCR




---

## Requirements

Python 3.7+
Streamlit
Pillow
Requests
A valid Groq API key

---
## Usage

Start the Streamlit app:
Copystreamlit run app.py

Open your web browser and go to http://localhost:8501
Upload an image (PNG, JPG, or JPEG, up to 200MB)
Select the desired Llama 3.2 vision model
Click "Extract Text" to process the image
View the extracted text formatted in Markdown

---

## How It Works
The application uses the Groq API to access Meta's Llama 3.2 vision models. When you upload an image, the application:

Converts the image to a base64-encoded string
Sends the image to the Groq API along with a prompt for text extraction
Processes the API response
Displays the extracted text in a formatted Markdown layout

---
