import streamlit as st
import streamlit.components.v1 as components

# Streamlit App Main Function
def main():
    st.title('TI-84 Plus Emulator')
    st.write("This is an example of embedding a TI-84 Plus emulator into a Streamlit app.")

    # Embed jsTIfied emulator using an iframe
    emulator_url = "https://www.cemetech.net/projects/jstified/"  # Replace with the hosted URL if needed
    iframe_code = f"""
    <iframe src="{emulator_url}" width="800" height="600" frameborder="0"></iframe>
    """
    components.html(iframe_code, height=600)

if __name__ == '__main__':
    main()