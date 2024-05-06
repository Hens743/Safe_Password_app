Got it! Here's the modified code with buttons styled according to the strength of the password length:

```python
import streamlit as st
import secrets
import string
import math
import qrcode
from io import BytesIO

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

st.title("Secure password generator with QR code")

# Predefined numbers with preselected buttons
st.subheader("Select a pre-defined password length:")
selected_length = st.radio("", ["5", "8", "10", "12", "15"])

# Option to enter a custom number
custom_length = st.text_input("Or enter a custom password length:")

# Choose between selected or custom length
if custom_length:
    length = int(custom_length)
else:
    length = int(selected_length)

# Color-coded buttons based on strength
st.markdown("#### Password Strength:")
if length < 8:
    button_color = "red"
elif length < 10:
    button_color = "orange"
elif length < 12:
    button_color = "yellow"
elif length < 15:
    button_color = "green"
else:
    button_color = "blue"

button_styles = {
    "color": "white",
    "background-color": button_color,
    "border-radius": "10px",
    "padding": "10px 20px",
    "font-size": "16px"
}

button_5 = st.button("5", key="button_5", style=button_styles)
button_8 = st.button("8", key="button_8", style=button_styles)
button_10 = st.button("10", key="button_10", style=button_styles)
button_12 = st.button("12", key="button_12", style=button_styles)
button_15 = st.button("15", key="button_15", style=button_styles)

# Arrange the first three checkboxes on the left and the last three on the right
col1, col2 = st.columns([1, 2])
with col1:
    include_letters = st.checkbox("Include letters", value=True)
    include_digits = st.checkbox("Include digits", value=True)
    include_punctuation = st.checkbox("Include punctuation", value=True)
with col2:
    include_specials = st.checkbox("Include special characters", value=False)
    include_scandinavian = st.checkbox("Include Scandinavian characters", value=False)
    include_icelandic = st.checkbox("Include Icelandic characters", value=False)

st.title ("Results")
hide_password = st.checkbox("Hide password", value=False)
display_qr_code = st.checkbox("Display as QR code", value=False)

if st.button("Generate password"):
    entropy = calculate_entropy(length, include_letters, include_digits, include_punctuation, include_specials, include_scandinavian, include_icelandic)
    password = generate_password(length, include_letters, include_digits, include_punctuation, include_specials, include_scandinavian, include_icelandic)
    if password:
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

# Recommended guidelines
st.sidebar.markdown("### Common guidelines")
st.sidebar.markdown("""
- Consider a minimum password length of 8 characters as a general guide. Both the US and UK cyber security departments recommend long and easily memorable passwords over short complex ones.
- Generate passwords randomly where feasible.
- Avoid using the same password twice (e.g. across multiple user accounts and/or software systems).
- Avoid character repetition, keyboard patterns, dictionary words, and sequential letters or numbers.
- Avoid using information that is or might become publicly associated with the user or the account, such as the user name, ancestors' names, or dates.
- Avoid using information that the user's colleagues and/or acquaintances might know to be associated with the user, such as relatives or pet names, romantic links (current or past), and biographical information (e

.g. ID numbers, ancestors' names or dates).
- Do not use passwords that consist wholly of any simple combination of the aforementioned weak components.
""")
