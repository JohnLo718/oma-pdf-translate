# PDF Translation App

This project provides a simple Streamlit application that translates the text in a PDF while trying to keep the original layout. It is intended for translating official documents where formatting matters.

## Features
- Upload a PDF file using the web interface.
- Choose a source language (English, German, or French).
- Choose a target language (Traditional Chinese or English).
- Download the translated PDF once processing is complete.

Translation quality depends on the translator backend. The included example uses `googletrans` for demonstration. For higher quality consider integrating the DeepL or OpenAI API.

## Local Setup
1. Install dependencies (Python 3.9+ recommended):
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Streamlit application:
   ```bash
   streamlit run main.py
   ```

## Docker
Build and run the app using Docker:
```bash
docker build -t pdf-translate .
docker run -p 8080:8080 pdf-translate
```

## Google Cloud Run Deployment
1. Build the container image and push to Google Container Registry (requires gcloud):
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/pdf-translate
   ```
2. Deploy to Cloud Run:
   ```bash
   gcloud run deploy pdf-translate \
     --image gcr.io/PROJECT_ID/pdf-translate \
     --platform managed \
     --region REGION \
     --port 8080
   ```

## Custom Translator
To use DeepL or GPT-4, modify `translate_text` in `main.py` to call the desired API. Example with DeepL:
```python
import deepl
translator = deepl.Translator("YOUR_API_KEY")
result = translator.translate_text(text, source_lang=src.upper(), target_lang=dest.upper())
return result.text
```

## Limitations
- Perfect layout preservation for complex PDFs is difficult. Some formatting loss may occur.
- Googletrans may fail on large texts or with strict rate limits.

This repository serves as a starting point for a production-ready solution.
