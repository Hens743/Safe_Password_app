import streamlit as st
import secrets
import string
import math
import qrcode

# Constants for character sets
LETTERS = string.ascii_letters
DIGITS = string.digits
PUNCTUATION = string.punctuation
SPECIALS = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`£µ" 
SCANDINAVIAN = "åäöÅÄÖåÅäÄöÖøØæÆ"
ICELANDIC = "áÁðÐéÉíÍóÓúÚýÝþÞ"

def calculate_entropy(length, character_set):
    """Calculates the entropy of a password given its length and character set."""
    if not character_set:
        return 0

    n = len(character_set)  # Number of possible characters
    entropy = math.log2(n ** length)
    return round(entropy)

def estimate_strength(entropy):
    """Estimates password strength based on its entropy."""
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

def generate_password(length, character_set):
    """Generates a secure random password."""
    if not character_set:
        st.error("Please select at least one character type.")
        return None  # Indicate failure

    password = ''.join(secrets.choice(character_set) for _ in range(length))
    return password

def display_qr_code(data):
    """Displays a QR code for the given data."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    st.image(img, caption="QR Code", use_column_width=True)

# Streamlit UI
st.title("Secure Password Generator")

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
    character_set = "".join(set for set in 
                            [LETTERS, DIGITS, PUNCTUATION, SPECIALS, SCANDINAVIAN, ICELANDIC]
                            if set in (include_letters, include_digits, include_punctuation,
                                      include_specials, include_scandinavian, include_icelandic))

    entropy = calculate_entropy(length, character_set)
    password = generate_password(length, character_set)

    if password:
        strength = estimate_strength(entropy)
        if hide_password:
            password_display = "*" * len(password)
        else:
            password_display = password

        data = {"Generated Password": password_display, "Strength": strength, "Entropy (bits)": entropy}
        st.table(data)

        if show_qr_code:
            display_qr_code(password)

# Recommended guidelines (Sidebar)
st.sidebar.markdown("### Common Guidelines")
# ... (Your guidelines text) 
