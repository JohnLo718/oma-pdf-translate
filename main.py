import io
import streamlit as st
import fitz  # PyMuPDF
from googletrans import Translator


def translate_text(text: str, translator: Translator, src: str, dest: str) -> str:
    if not text.strip():
        return text
    try:
        result = translator.translate(text, src=src, dest=dest)
        return result.text
    except Exception as e:
        st.warning(f"Translation failed: {e}")
        return text


def translate_pdf(data: bytes, src_lang: str, tgt_lang: str) -> bytes:
    """Translate PDF text while trying to preserve layout."""
    doc = fitz.open(stream=data, filetype="pdf")
    translator = Translator()

    for page in doc:
        text_page = page.get_text("dict")
        for block in text_page.get("blocks", []):
            for line in block.get("lines", []):
                line_text = " ".join(span["text"] for span in line.get("spans", []))
                if not line_text.strip():
                    continue
                translated = translate_text(line_text, translator, src_lang, tgt_lang)
                bbox = fitz.Rect(line["bbox"])
                page.add_redact_annot(bbox, fill=(1, 1, 1))
                page.apply_redactions()
                page.insert_text((bbox.x0, bbox.y1 - 2), translated, fontsize=12)

    output = io.BytesIO()
    doc.save(output)
    return output.getvalue()


LANG_OPTIONS = {
    "English": "en",
    "German": "de",
    "French": "fr",
}

TARGET_OPTIONS = {
    "Traditional Chinese": "zh-tw",
    "English": "en",
}

st.set_page_config(page_title="PDF Translation App")
st.title("PDF Translation App")

uploaded_pdf = st.file_uploader("Upload PDF", type="pdf")

col1, col2 = st.columns(2)
with col1:
    src_lang_label = st.selectbox("Source Language", list(LANG_OPTIONS.keys()))
with col2:
    tgt_lang_label = st.selectbox("Target Language", list(TARGET_OPTIONS.keys()))

if st.button("Translate") and uploaded_pdf:
    st.warning(
        "Layout may not be perfectly preserved in the translated PDF.",
        icon="⚠️",
    )
    src_lang = LANG_OPTIONS[src_lang_label]
    tgt_lang = TARGET_OPTIONS[tgt_lang_label]
    with st.spinner("Translating..."):
        result_bytes = translate_pdf(uploaded_pdf.read(), src_lang, tgt_lang)
    st.success("Translation complete.")
    st.download_button(
        "Download translated PDF",
        result_bytes,
        file_name="translated.pdf",
        mime="application/pdf",
    )
