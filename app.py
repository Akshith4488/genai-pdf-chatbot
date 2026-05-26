import streamlit as st
from openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
from docx import Document
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

st.title("GenAI DOC Chatbot")

uploaded_file = st.file_uploader(
    "Upload a document",
    type=["pdf", "docx"]
)

if uploaded_file:

    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.read())

    file_text = ""

    if uploaded_file and uploaded_file.name.endswith(".pdf"):

                        loader = PyPDFLoader(uploaded_file.name)
                        
                        pages = loader.load()
                        
                       

                        for page in pages:
                            file_text += page.page_content
                            

    elif uploaded_file and uploaded_file.name.endswith(".docx"):

        doc = Document(uploaded_file.name)

        for para in doc.paragraphs:
           file_text += para.text
        


    st.success("File Loaded Successfully!")

    question = st.text_input("Ask question from File:")


    if question:

        prompt = f"""
        Answer the question based on the File content below.

        File Content:
        {file_text}

        Question:
        {question}
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

        st.write(answer)