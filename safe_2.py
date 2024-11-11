import streamlit as st
import secrets
import string
import math
import qrcode
from io import BytesIO
import matplotlib.pyplot as plt

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
    if include_sami:
        characters += "ÁáĐđŊŋŠšŽžÅåÄäÖö"  # Sami characters

    if not characters:
        st.error("Please select at least one character type.")
        return
    
    password = ''.join((secrets.choice(characters) for _ in range(length)))
    return password

def display_entropy_graph(entropy):
    strength = estimate_strength(entropy)
    color_map = {
        "Very Weak": "red",
        "Weak": "orange",
        "Moderate": "yellow",
        "Strong": "blue",
        "Very Strong": "green"
    }
    color = color_map.get(strength, "gray")
    
    # Plot the entropy score
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.barh(['Entropy'], [entropy], color=color)
    ax.set_xlim(0, 128)  # Set x-axis limit based on entropy range
    ax.set_xlabel("Entropy Score (bits)")
    ax.set_title(f"Password Strength: {strength}")
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)

    st.pyplot(fig)

st.title("Secure password generator with QR code (NO/SE/FI/ICL + Sami)")

length = st.number_input("Length of password", min_value=1, value=8, step=1)

col1, col2 = st.columns([1, 2])
with col1:
    include_letters = st.checkbox("Include letters", value=True)
    include_digits = st.checkbox("Include digits", value=True)
    include_punctuation = st.checkbox("Include punctuation", value=True)
with col2:
    include_specials = st.checkbox("Include special characters", value=False)
    include_scandinavian = st.checkbox("Include Scandinavian characters", value=False)
    include_icelandic = st.checkbox("Include Icelandic characters", value=False)
    include_sami = st.checkbox("Include Sami characters", value=False)

st.title("Results")
hide_password = st.checkbox("Hide password", value=False)
display_qr_code = st.checkbox("Display as QR code", value=False)

if "password" not in st.session_state:
    st.session_state.password = ""
    st.session_state.entropy = 0

def generate_and_display_password():
    entropy = calculate_entropy(length, include_letters, include_digits, include_punctuation, include_specials, include_scandinavian, include_icelandic)
    password = generate_password(length, include_letters, include_digits, include_punctuation, include_specials, include_scandinavian, include_icelandic)
    st.session_state.password = password
    st.session_state.entropy = entropy
    strength = estimate_strength(entropy)

    if hide_password:
        password_display = "*" * len(password)
    else:
        password_display = password

    data = {"Generated password": password_display, "Strength": strength, "Entropy (bits)": entropy}
    st.table(data)

    # Show entropy score graph
    display_entropy_graph(entropy)

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
