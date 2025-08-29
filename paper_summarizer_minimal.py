# paper_summarizer_minimal.py
import streamlit as st
import PyPDF2
import os
import openai
from io import BytesIO

st.set_page_config(page_title="AI Research Paper Summarizer", layout="wide")
st.title("📄 AI Research Paper Summarizer - Minimal")

# Load API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ No API key found. Please set OPENAI_API_KEY first.")
else:
    openai.api_key = api_key

# Upload PDF
pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])
if pdf_file is not None:
    try:
        reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        st.success(f"✅ Extracted text from {len(reader.pages)} pages.")

        # Show preview
        if st.checkbox("Show first 1000 characters of extracted text"):
            st.text(text[:1000])

        # Generate summary
        if st.button("✨ Generate Summary"):
            with st.spinner("Summarizing..."):
                prompt = f"Summarize the following research paper in 3-5 sentences:\n\n{text[:2000]}"
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=500,
                        temperature=0.0,
                    )
                    summary = response["choices"][0]["message"]["content"]
                    st.subheader("🔑 Summary")
                    st.write(summary)
                except Exception as e:
                    st.error(f"OpenAI error: {e}")
    except Exception as e:
        st.error(f"PDF extraction error: {e}")
