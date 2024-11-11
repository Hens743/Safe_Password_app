import streamlit as st
import secrets
import string
import math
import qrcode
from io import BytesIO
import random

# Password entropy calculation function
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
    if include_sami:
        characters += "ÁáĐđŊŋŠšŽžÅåÄäÖö"  # Sami characters
    
    if not characters:
        return 0
    
    N = len(characters)
    entropy = math.log2(N ** length)
    return round(entropy)

# Password strength estimator
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

# Password generator function
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
    if include_sami:
        characters += "ÁáĐđŊŋŠšŽžÅåÄäÖö"  # Sami characters

    if not characters:
        st.error("Please select at least one character type.")
        return
    
    password = ''.join((secrets.choice(characters) for _ in range(length)))
    return password

# UI Elements
st.title("Secure password generator with QR code (NO/SE/FI/ICL + Sami)")

length = st.number_input("Length of password", min_value=1, value=8, step=1)

# Toggle buttons to select character types
if "include_letters" not in st.session_state:
    st.session_state.update({
        "include_letters": True,
        "include_digits": True,
        "include_punctuation": True,
        "include_specials": False,
        "include_scandinavian": False,
        "include_icelandic": False,
        "include_sami": False
    })

col1, col2 = st.columns([1, 2])
with col1:
    if st.button("Toggle letters"):
        st.session_state.include_letters = not st.session_state.include_letters
    st.write(f"Include letters: {'Yes' if st.session_state.include_letters else 'No'}")

    if st.button("Toggle digits"):
        st.session_state.include_digits = not st.session_state.include_digits
    st.write(f"Include digits: {'Yes' if st.session_state.include_digits else 'No'}")

    if st.button("Toggle punctuation"):
        st.session_state.include_punctuation = not st.session_state.include_punctuation
    st.write(f"Include punctuation: {'Yes' if st.session_state.include_punctuation else 'No'}")

with col2:
    if st.button("Toggle special characters"):
        st.session_state.include_specials = not st.session_state.include_specials
    st.write(f"Include special characters: {'Yes' if st.session_state.include_specials else 'No'}")

    if st.button("Toggle Scandinavian characters"):
        st.session_state.include_scandinavian = not st.session_state.include_scandinavian
    st.write(f"Include Scandinavian characters: {'Yes' if st.session_state.include_scandinavian else 'No'}")

    if st.button("Toggle Icelandic characters"):
        st.session_state.include_icelandic = not st.session_state.include_icelandic
    st.write(f"Include Icelandic characters: {'Yes' if st.session_state.include_icelandic else 'No'}")

    if st.button("Toggle Sami characters"):
        st.session_state.include_sami = not st.session_state.include_sami
    st.write(f"Include Sami characters: {'Yes' if st.session_state.include_sami else 'No'}")

st.title("Results")
hide_password = st.checkbox("Hide password", value=False)
display_qr_code = st.checkbox("Display as QR code", value=False)

if "password" not in st.session_state:
    st.session_state.password = ""
    st.session_state.entropy = 0

def generate_and_display_password():
    entropy = calculate_entropy(
        length, 
        st.session_state.include_letters, 
        st.session_state.include_digits, 
        st.session_state.include_punctuation, 
        st.session_state.include_specials, 
        st.session_state.include_scandinavian, 
        st.session_state.include_icelandic
    )
    password = generate_password(
        length, 
        st.session_state.include_letters, 
        st.session_state.include_digits, 
        st.session_state.include_punctuation, 
        st.session_state.include_specials, 
        st.session_state.include_scandinavian, 
        st.session_state.include_icelandic
    )

    st.session_state.password = password
    st.session_state.entropy = entropy
    strength = estimate_strength(entropy)

    if hide_password:
        password_display = "*" * len(password)
    else:
        password_display = password

    data = {"Generated password": password_display, "Strength": strength, "Entropy (bits)": entropy}
    st.table(data)

    if display_qr_code:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(password)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        st.image(img_bytes, caption="Password QR Code", use_column_width=True)

# Generate Password button (also serves as "Regenerate" button)
if st.button("Generate password"):
    generate_and_display_password()

# Copy to clipboard button (JavaScript snippet to copy password)
if st.button("Copy"):
    st.write(f"<script>navigator.clipboard.writeText('{st.session_state.password}');</script>", unsafe_allow_html=True)
    st.success("Password copied to clipboard!")
