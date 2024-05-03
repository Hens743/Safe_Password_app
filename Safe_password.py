import streamlit as st
import secrets
import string
import math
import qrcode
from qrcode.image.pil import PilImage
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

def calculate_entropy(length, include_letters=True, include_digits=True, include_punctuation=True, include_specials=False, include_scandinavian=False, include_icelandic=False):
    characters = ""
    if include_letters:
        characters += string.ascii_letters
    if include_digits:
        characters += string.digits
    if include_punctuation:
        characters += string.punctuation
    if include_specials:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?/~`£µ"
    if include_scandinavian:
        characters += "åäöÅÄÖåÅäÄöÖøØæÆ"  # Scandinavian characters
    if include_icelandic:
        characters += "áÁðÐéÉíÍóÓúÚýÝþÞ"  # Icelandic characters
    
    if not characters:
        return 0
    
    N = len(characters)
    entropy = math.log2(N ** length)
    return round(entropy)

def estimate_strength(entropy):
    if entropy < 28:
        return "Very Weak"
    elif entropy < 56:
        return "Weak"
    elif entropy < 84:
        return "Moderate"
    elif entropy < 112:
        return "Strong"
    else:
        return "Very Strong"

def generate_password(length, include_letters=True, include_digits=True, include_punctuation=True, include_specials=False, include_scandinavian=False, include_icelandic=False):
    characters = ""
    if include_letters:
        characters += string.ascii_letters
    if include_digits:
        characters += string.digits
    if include_punctuation:
        characters += string.punctuation
    if include_specials:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?/~`£µ"
    if include_scandinavian:
        characters += "åäöÅÄÖåÅäÄöÖøØæÆ"  # Scandinavian characters
    if include_icelandic:
        characters += "áÁðÐéÉíÍóÓúÚýÝþÞ"  # Icelandic characters
    
    if not characters:
        st.error("Please select at least one character type.")
        return
    
    password = ''.join((secrets.choice(characters) for _ in range(length)))
    return password

def display_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white", image_factory=PilImage)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode()
    return img_base64

# Streamlit app title
st.title("Secure Password Generator with QR Code")

# Options for generating the password
length = st.number_input("Length of Password", min_value=1, value=8, step=1)
include_letters = st.checkbox("Include Letters", value=True)
include_digits = st.checkbox("Include Digits", value=True)
include_punctuation = st.checkbox("Include Punctuation", value=True)
include_specials = st.checkbox("Include Special Characters", value=False)
include_scandinavian = st.checkbox("Include Scandinavian Characters", value=False)
include_icelandic = st.checkbox("Include Icelandic Characters", value=False)
hide_password = st.checkbox("Hide Password", value=False)
show_qr_code = st.checkbox("Show QR Code", value=False)

if st.button("Generate Password"):
    entropy = calculate_entropy(length, include_letters, include_digits, include_punctuation, include_specials, include_scandinavian, include_icelandic)
    password = generate_password(length, include_letters, include_digits, include_punctuation, include_specials, include_scandinavian, include_icelandic)
    if password:
        strength = estimate_strength(entropy)
        if hide_password:
            password_display = "*" * len(password)
        else:
            password_display = password
        
        data = {"Generated Password": password_display, "Strength": strength, "Entropy (bits)": entropy}
        st.table(data)
        
        if show_qr_code:
            qr_code_base64 = display_qr_code(password)
            qr_code_html = f'<img src="data:image/png;base64,{qr_code_base64}" alt="QR Code">'
            st.markdown(qr_code_html, unsafe_allow_html=True)

# Recommended guidelines
st.sidebar.markdown("### Common Guidelines")
st.sidebar.markdown("""
- Consider a minimum password length of 8 characters as a general guide. Both the US and UK cyber security departments recommend long and easily memorable passwords over short complex ones.
- Generate passwords randomly where feasible.
- Avoid using the same password twice (e.g. across multiple user accounts and/or software systems).
- Avoid character repetition, keyboard patterns, dictionary words, and sequential letters or numbers.
- Avoid using information that is or might become publicly associated with the user or the account, such as the user name, ancestors' names, or dates.
- Avoid using information that the user's colleagues and/or acquaintances might know to be associated with the user, such as relatives or pet names, romantic links (current or past), and biographical information (e.g. ID numbers, ancestors' names or dates).
- Do not use passwords that consist wholly of any simple combination of the aforementioned weak components.
""")
