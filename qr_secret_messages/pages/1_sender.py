import streamlit as st
import os

st.set_page_config(page_title="Sender")

st.title("📤 Sender — Upload QR Image")

uploaded_qr = st.file_uploader(
    "Upload encrypted QR code image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_qr:
    os.makedirs("shared", exist_ok=True)

    with open("shared/qr.png", "wb") as f:
        f.write(uploaded_qr.read())

    st.success("QR image sent successfully!")
    st.image("shared/qr.png", caption="Sent QR Code")
