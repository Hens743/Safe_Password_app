import streamlit as st
import random
import string
import secrets
import qrcode
from PIL import Image

# Function to generate a random string of lowercase letters of given length
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# Function to generate a random string of letters (lowercase and uppercase) and digits of given length
def get_random_password(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Function to generate a secure random string of given length
def get_secure_random_string(length):
    secure_str = ''.join((secrets.choice(string.ascii_letters) for i in range(length)))
    return secure_str

# Function to generate a random alphanumeric string of letters and digits of given length
def get_random_alphanumeric_string(length):
    source = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(source) for i in range(length)))
    return result_str

# Function to generate a QR code with the given data
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# Streamlit UI
st.title("Random String and QR Code Generator")

# Generate random string of lowercase letters
length_lower = st.slider("Select length for lowercase random string:", 1, 20, 8)
if st.button("Generate Random Lowercase String"):
    random_lower_string = get_random_string(length_lower)
    st.write("Random Lowercase String:", random_lower_string)

# Generate random password
length_password = st.slider("Select length for random password:", 1, 20, 8)
if st.button("Generate Random Password"):
    random_password = get_random_password(length_password)
    st.write("Random Password:", random_password)

# Generate secure random string
length_secure = st.slider("Select length for secure random string:", 1, 20, 8)
if st.button("Generate Secure Random String"):
    secure_random_string = get_secure_random_string(length_secure)
    st.write("Secure Random String:", secure_random_string)

# Generate random alphanumeric string
length_alphanumeric = st.slider("Select length for random alphanumeric string:", 1, 20, 8)
if st.button("Generate Random Alphanumeric String"):
    random_alphanumeric_string = get_random_alphanumeric_string(length_alphanumeric)
    st.write("Random Alphanumeric String:", random_alphanumeric_string)

# Generate QR code
qr_data = st.text_input("Enter data for QR code:")
if st.button("Generate QR Code"):
    if qr_data:
        qr_image = generate_qr_code(qr_data)
        st.image(qr_image, caption="Generated QR Code", use_column_width=True)
    else:
        st.warning("Please enter data for QR code")
