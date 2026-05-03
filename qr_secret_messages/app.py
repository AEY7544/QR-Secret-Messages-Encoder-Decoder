import streamlit as st

st.set_page_config(page_title="QR Secret Messages", layout="centered")

st.title("🔐 QR Code Secret Messages")
st.write(
    """
    Use the **Sender** page to upload a QR image.
    Use the **Receiver** page to receive and decrypt it.
    Both users must be on the same network.
    """
)
