import streamlit as st
import requests
import numpy as np
import streamlit.components.v1 as components
import asyncio
import re
import pandas as pd
st.markdown(
    """
    <style>
    /* Set the main background with a light mode and optional picture */
    .stApp {
        background: #ffffff; /* Light mode background color */
        background-image: url("/cimages/multimages/16/system2401008797131253426.png"); /* Optional background picture */
        background-size: cover;
        color: #000000; /* Black text for light mode */
    }

    /* Set the sidebar background with a light mode and optional picture */
    section[data-testid="stSidebar"] {
        background: #ffffff; /* Light gray background for sidebar */
        background-image: url("Graph3.gif"); /* Optional sidebar picture */
        background-size: cover;
        color: #000000; /* Black text for light mode */
    }

    /* Ensure text is readable on light backgrounds */
    .stMarkdown, .stTextInput, .stButton {
        color: #000000; /* Black text */
    }
    </style>
    """,
    unsafe_allow_html=True
)
with st.sidebar:
    st.title("Steps")
    st.write("1. Make sure both equations are solved for y.")
    st.write("2. Substitute the linear equation into the quadratic equation.")
    st.write("3. Solve the quadratic equation using factoring.")
    st.write("4. Plug the solutions into the linear equation to find the y-values.")
    st.write("5. Write the solutions as ordered pairs (x, y).")
    st.title("Have fun!")
st.title('LINEAR-QUADRATIC SYSTEMS')

st.write('This is a quadratic-linear system generator.')

# User input
question = st.text_input("Enter any questions you have about linear-quadratic systems: ")

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

quad_system_response = requests.get(
    'https://first-api-y6hb.onrender.com/quadratic-system'
)


# Display the equations in Streamlit
st.write('Shown below is a quadratic function and a linear function, both solved for y:')
quadratic_equation = quad_system_response.json()['quadratic_function']
linear_equation = quad_system_response.json()['linear_function']
solutions = quad_system_response.json()['solutions']

st.latex(quadratic_equation)
st.latex(linear_equation)


# API Call (for chatbot response)


# Function to integrate Desmos graph
def desmos_integration(quadratic_eq, linear_eq, solution_set=None):
    
    desmos_script = f"""
    <script src="https://www.desmos.com/api/v1.6/calculator.js?apiKey=dcb31709b452b1cf9dc26972add0fda6"></script>
    <div id="calculator" style="width: 1000px; height: 1000px;length: 1000px"></div>
    <script>
        var elt = document.getElementById('calculator');
        var calculator = Desmos.GraphingCalculator(elt, {{
            settings: {{
                invertColors: true  // Enable reverse contrast (dark mode)
            }}
        }});
        calculator.setExpression({{ latex: "{quadratic_eq.replace(' ', '')}" }});
        calculator.setExpression({{ latex: "{linear_eq.replace(' ', '')}" }});
        calculator.setExpression({{ latex: "{solutions[0]}", showLabel: true }});
        calculator.setExpression({{ latex: "{solutions[1]}", showLabel: true }});
    </script>
    """
    components.html(desmos_script, height=500)

# Streamlit App Main Function
def main():
    st.title('Finding solutions graphically')
    st.write("The first way to find a solution to the system is to graph both equations and find their intersection points.")
    st.write("Use your scroll button to zoom in and out of the graph. You can also click and drag to move the graph around.")
    st.write('The solutions are:')
    st.latex(solutions[0] + ',' + solutions[1])
    # Pass the dynamically generated equations to Desmos
    desmos_integration(quadratic_equation, linear_equation)
    st.write('You can also check the table of values to find the intersection points....')
    # Get the table of values from the API response
    table_of_values = pd.DataFrame(quad_system_response.json()['table of values'])

    # Define a function to highlight rows where the linear and quadratic values are equal
    def highlight_equal_rows(row):
        linear_col = table_of_values.columns[1]  # Assuming the second column is the linear function
        quadratic_col = table_of_values.columns[2]  # Assuming the third column is the quadratic function
        if row[linear_col] == row[quadratic_col]:
            return ['background-color: green'] * len(row)
        else:
            return [''] * len(row)

    # Apply the highlighting function
    styled_table = table_of_values.style.apply(highlight_equal_rows, axis=1)

    # Display the styled DataFrame in Streamlit
    st.dataframe(styled_table, width=400, height=400)
    
    
    

    st.title('Finding solutions algebraically')
    st.write("The second way to find a solution to the system is to solve the system algebraically. Here are the steps:")
    st.write("1. Solve the linear equation for y.(in this case, both already are solved for y)")
    st.latex(linear_equation)
    st.latex(quadratic_equation)
    st.write("2. Substitute the linear equation into the quadratic equation.")
    quadratic_withouty = quadratic_equation[4:]
    linear_withouty = linear_equation[4:]
    st.latex(quadratic_withouty + ' = ' + linear_withouty)
    st.write("move all terms to one side of the equation to get:")
    st.latex(quad_system_response.json()['factored_function'])
    
    st.write("3. Solve the quadratic equation using factoring.")
    st.latex(quad_system_response.json()['factors'])
    st.latex(quad_system_response.json()['roots'][0])
    st.write("4. Plug them into the linear equation to find the y-values.")
    st.latex(linear_equation)
    st.latex(quad_system_response.json()['substitution'][0])
    st.latex(quad_system_response.json()['substitution'][1])
    st.write("5. Write the solutions as ordered pairs (x, y).")
    st.latex(quad_system_response.json()['solutions'][0] + ','+ quad_system_response.json()['solutions'][1])



if __name__ == '__main__':
    main()
