import streamlit as st
import requests
import numpy as np
import streamlit.components.v1 as components
from agents import Agent
from agents import Runner
import asyncio
import re
st.title('LINEAR-QUADRATIC SYSTEMS')

st.write('This is a simple chatbot that uses the OpenAI API to answer questions. Please enter your question below.')

# User input
question = st.text_input("Enter your question: ")

# Generate random coefficients for quadratic and linear functions

a = np.random.randint(-2, 2)
b = np.random.randint(-10, 10)
c = np.random.randint(-10, 10)
m = np.random.randint(-5, 5)
b_linear = np.random.randint(-10, 10)

# Display the equations in Streamlit
quadratic_equation = f"y = x^2 + {a+b}x + {a*c}"
linear_equation = f"y = {m}x + {b_linear}"

st.latex(quadratic_equation)
st.latex(linear_equation)

# API Call (for chatbot response)
if question:
    response = requests.get(
        'https://first-api-y6hb.onrender.com/chatbot',
        params={'prompt': f"Answer this question: {question}"}
    )
    if response.status_code == 200:
        answer = response.json().get('answer', 'No response received.')
        st.write("Response:", answer)
    else:
        st.write("Error fetching response from API.")

# Function to integrate Desmos graph
def desmos_integration(quadratic_eq, linear_eq):
    desmos_script = f"""
    <script src="https://www.desmos.com/api/v1.6/calculator.js?apiKey=dcb31709b452b1cf9dc26972add0fda6"></script>
    <div id="calculator" style="width: 600px; height: 800px;length: 800px"></div>
    <script>
        var elt = document.getElementById('calculator');
        var calculator = Desmos.GraphingCalculator(elt);
        calculator.setExpression({{ latex: "{quadratic_eq.replace(' ', '')}" }});
        calculator.setExpression({{ latex: "{linear_eq.replace(' ', '')}" }});
    </script>
    """
    components.html(desmos_script, height=500)

# Streamlit App Main Function
def main():
    st.title('Desmos Integration with Streamlit')
    st.write("This is an example of integrating Desmos into a Streamlit web application.")

    # Pass the dynamically generated equations to Desmos
    desmos_integration(f"y={a}x^2+{b}x+{c}", f"y={m}x+{b_linear}")

if __name__ == '__main__':
    main()
