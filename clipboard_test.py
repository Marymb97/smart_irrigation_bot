import streamlit as st
try:
    from streamlit_clipboard import clipboard
    st.success("streamlit-clipboard is available!")
    clipboard("Hello world!", label="Copy Hello", help="Copy test")
except ImportError:
    st.error("streamlit-clipboard is NOT available.")
