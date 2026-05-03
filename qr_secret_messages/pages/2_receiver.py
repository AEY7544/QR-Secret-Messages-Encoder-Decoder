import streamlit as st
import os

from crypto_utils import decrypt_message
from qr_utils import read_qr

st.set_page_config(page_title="Receiver")

st.title("📥 Receiver — Decrypt QR")

if not os.path.exists("shared/qr.png"):
    st.warning("No QR image received yet.")
else:
    st.image("shared/qr.png", caption="Received QR Code")

    password = st.text_input("Decryption Password", type="password")

    if st.button("Decrypt Message"):
        if not password:
            st.error("Password required")
        else:
            try:
                encrypted_data = read_qr("shared/qr.png")
                decrypted = decrypt_message(encrypted_data, password)

                st.success("Decrypted Message:")
                st.write(decrypted)
            except Exception:
                st.error("Wrong password or invalid QR code")
