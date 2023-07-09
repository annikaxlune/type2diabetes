import streamlit as st

bg_image="""<style>
[data-testid="stAppViewContainer"]{
background-color: #e5e5f7;
opacity: 0.8;
background-image: radial-gradient(circle at center center, #444cf7, #e5e5f7), repeating-radial-gradient(circle at center center, #444cf7, #444cf7, 10px, transparent 20px, transparent 10px);
background-blend-mode: multiply;
}
</style>"""
st.markdown(bg_image,
            unsafe_allow_html=True)
st.title("It's summer")