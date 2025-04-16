import streamlit as st
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# App title and description
st.markdown("<h3 style='text-align: center;'>Algebra Practice - Linear/Quadratic Systems</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Pick a level of a problem you want to try. (For Algebra I, choose level 1 to start):</h3>", unsafe_allow_html=True)

# Create three columns for buttons
left, middle, right = st.columns(3)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize a variable to store the button prompt
button_prompt = None

# Check which button is clicked and set the prompt accordingly
if left.button("Level 1 - Already Solved for y", icon="😃", use_container_width=True):
    button_prompt = "Give me a linear-quadratic system of equations where both the linear and quadratic system already are solved for y. " \
    "Make sure the intersection points are integers for the coordinates. Then tell me the solution. A solution is defined as the intersection points."

if middle.button("Level 2 - Need to solve for y", icon="😊", use_container_width=True):
    button_prompt = "Give me a linear-quadratic system of equations where the quadratic equation is already are solved for y, but the linear equation is not. " \
    "Make sure the intersection points are integers for the coordinates. Then tell me the solution. A solution is defined as the intersection points."

if right.button("Level 3 - non-integer answers", icon="😏", use_container_width=True):
    button_prompt = "Give me a linear-quadratic system of equations where the quadratic equation is already are solved for y, but the linear equation is not. " \
    "The intersection points do not have to be integers, but they should be rational numbers. Then tell me the solution. A solution is defined as the intersection points."

# If a button was clicked, simulate the chat input
if button_prompt:
    # Add the button prompt to chat history
    st.session_state.messages.append({"role": "user", "content": button_prompt})

    # Generate response using OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        )
        answer = response.choices[0].message["content"]
    except Exception as e:
        answer = f"An error occurred: {e}"

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_input := st.chat_input("Pick a level you want to try or ask a question"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate response using OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        )
        answer = response.choices[0].message["content"]
    except Exception as e:
        answer = f"An error occurred: {e}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(answer)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})