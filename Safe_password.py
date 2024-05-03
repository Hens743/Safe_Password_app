import streamlit as st
import qrcode
from PIL import Image
import io
import base64
from urllib.parse import urlparse

# Function to convert image to base64
def get_image_as_base64(image: Image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

def get_url_filename(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    main_domain = domain.split('.')
    main_domain = main_domain[1] if main_domain[0] == 'www' else main_domain[0]
    path = parsed_uri.path.strip('/').replace('/', '_')
    return f"{main_domain}_{path}" if path else main_domain

# Streamlit app title
st.title("Bulk QR Code Generator")
st.write("This is a simple Streamlit web app for generating QR codes based on user input. You can choose between generating a QR code for a URL or plain text with the ability to generate multiple URLs at once.")

# QR code content options
qr_content_options = ["URL", "Text"]
qr_content_type = st.selectbox("Select QR content type", qr_content_options)

# Content input based on selection
if qr_content_type == "URL":
    content = st.text_area("Enter URLs (one per line)", height=150)
else:
    content = st.text_area("Enter text (one per line)", height=150)

# Generate QR code button
if st.button("Generate QR Code"):
    if content:
        # Split content by lines
        contents = content.split("\n")

        for i, c in enumerate(contents):
            if c.strip():
                # Generate QR code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=10,
                    border=4
                )
                qr.add_data(c)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")

                # Convert image to bytes-like object
                img_bytes = io.BytesIO()
                img.save(img_bytes, format="PNG")

                # Display QR code
                st.markdown(f"#### {c}")
                st.image(img_bytes, caption=f"QR code for {c}", use_column_width=True)

                # Download link for QR code
                file_name = get_url_filename(c) if qr_content_type == "URL" else f"QR_{i}"
                st.markdown(f'[Download QR code](data:image/png;base64,{base64.b64encode(img_bytes.getvalue()).decode()};charset=utf-8;base64),{file_name}.png', unsafe_allow_html=True)
    else:
        st.error("Please enter content for the QR code.")
