import os
import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
from PIL import Image
from dotenv import load_dotenv
load_dotenv()
GOOGLE_KEY = st.secrets['GOOGLE_ACCESS_TOKEN']
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
print("We are good to go")
def get_gemini_response(input_prompt,input):
  model = genai.GenerativeModel('gemini-pro')
  response = model.generate_content([input_prompt, input])
  return response.text

def input_pdf_text(uploaded_file):
  reader = pdf.PdfReader(uploaded_file)
  text = ""
  for page in range(len(reader.pages)):
    page = reader.pages[page]
    text+=str(page.extract_text())
    return text
    
# Prompt template
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume. 
Please share your professional evaluation on whether the candidate's profile aligns with the given role . 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
Your task is to evaluate the resume based on the given job description. Give me the percentage of match if the resume matches the job description. 
First the output should come as percentage and then keywords missing for the job description and last final thoughts and then suggestions to improve the resume match.
"""
#input_prompt2 = """
#Hey Act Like a skilled or very experience ATS(Application Tracking System)
#with a deep understanding of tech field,software engineering,data science ,data analyst
#and big data engineer. Your task is to evaluate the resume based on the given job description.
#You must consider the job market is very competitive and you should provide 
#best assistance for improving thr resumes. Assign the percentage Matching based 
#on Jd and the missing keywords with high accuracy
#"""

##Streamlit app
img = Image.open("img/headhunting.png")
st.set_page_config(page_title="ATS Resume Expert", page_icon=img, initial_sidebar_state="expanded")
st.header("ATS Tracking System")

with st.sidebar:
  st.image("img/ats-resume-checker.png")
  st.write("---")
  st.title("About")
  st.write(
    """Our web application is built using Streamlit and leverages API requests from the Gemini Pro model to provide a powerful 
    and efficient Applicant Tracking System (ATS) for your recruitment needs.  We integrate with the Gemini Pro model, which is a state-of-the-art Language Model (LLM) trained specifically for handling recruitment tasks. This model is capable of understanding job descriptions, resumes,
    and candidate profiles with high accuracy and efficiency.
  """)

  st.markdown(
            """
            ---
            Follow me on:

            Github → [@tarunsehgal27](https://github.com/tarunsehgal27)

            LinkedIn → [Tarun Sehgal](https://www.linkedin.com/in/tarunsehgal27)

            """
        )

input_text = st.text_area("Job Description: ", key="input")
st.write(f'{len(input_text)} characters')
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
  st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me about my resume")
submit2 = st.button("Percentage match")

if submit1:
  with st.spinner("Processing"):
    if uploaded_file is not None:
      text = input_pdf_text(uploaded_file)
      response = get_gemini_response(input_prompt1, text)
      #st.subheader("Here's what we got for you!")
      col1, col2 = st.columns([1,1])
      with col1:
        st.subheader("Here's what we got for you")
      with col2:
        st.image("img/accept.png", width=40)

      #st.image(".png")
      st.write(response)
    else:
      st.write("Oops! No file uploaded. Please select a file to proceed.")

if submit2:
  with st.spinner("Processing"):
    if uploaded_file is not None:
      text = input_pdf_text(uploaded_file)
      response = get_gemini_response(input_prompt2, text)
      #st.subheader("The Response is")
      col1, col2 = st.columns([1,1])
      with col1:
        st.subheader("Here's what we got for you")
      with col2:
        st.image("img/accept.png", width=40)
      st.write(response)
    else:
      st.write("Oops! No file uploaded. Please select a file to proceed.")

st.markdown(
        """
        <div style="position: float; bottom: 0; left: 0; width: 100%; padding: 15px; text-align: center;">
            © <a href="https://github.com/tarunsehgal27" target="_blank">Tarun Sehgal</a> | <strong>Made with ❤️ </strong>
        </div>
        """,
        unsafe_allow_html=True
    )
