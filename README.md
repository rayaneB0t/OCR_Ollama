# Llama 3.2 Vision OCR


<img width="1375" alt="Screenshot 2025-04-02 at 18 09 24" src="https://github.com/user-attachments/assets/6b90bcd6-4f4c-4afe-9940-038141c47b76" />



## Requirements

- Python 3.7+
- Streamlit
- Pillow
- Requests
- A valid Groq API key


## How It Works
The application uses the Groq API to access Meta's Llama 3.2 vision models. When you upload an image, the application:

Converts the image to a base64-encoded string
Sends the image to the Groq API along with a prompt for text extraction
Processes the API response
Displays the extracted text in a formatted Markdown layout

---
