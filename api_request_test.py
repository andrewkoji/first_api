# import requests
# import time

# base_url = 'https://first-api-y6hb.onrender.com/chatbot'

# # Prompt the user for input
# user_prompt = input("Ask anything: ")

# # Pass the user input to the API
# params = {'prompt': user_prompt}

# if user_prompt:
#     print('just a sec...')
#     time.sleep(1)
#     response = requests.get(base_url, params=params)
#     print('\n')
#     # Print the response from the API
#     print(response.json()['answer'])

    
    
import requests
import pandas as pd
import pdfplumber

def extract_pdf_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        return " ".join(page.extract_text() or '' for page in pdf.pages)

def extract_excel_text(file_path):
    df = pd.read_excel(file_path)
    return df.to_string()


file_path = input("For your question, enter the file path of any information that will help me answer your questions: ")
question = input("Enter your question: ")

# Extract text from the file
if file_path.endswith('.pdf'):
    content = extract_pdf_text(file_path)
elif file_path.endswith(('.xls', '.xlsx')):
    content = extract_excel_text(file_path)
else:
    raise ValueError("Unsupported file type.")

# Send extracted text and question to the API
response = requests.get(
    'https://first-api-y6hb.onrender.com/chatbot',
    params={'prompt': f"Based on this content: {content}\nQuestion: {question}"}
)

print(response.json()['answer'])
