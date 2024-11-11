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

def create_password_from_words(input_words):
    words = input_words.split()
    password = ''.join(words)
    return password

st.title("Secure password generator with QR code (NO/SE/FI/ICL + Sami)")

# Options for generating the password
length = st.number_input("Length of password", min_value=1, value=8, step=1)

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
    include_sami = st.checkbox("Include Sami characters", value=False)

# New option to create password from input words
use_input_words = st.checkbox("Use input words to create password", value=False)
input_words = st.text_input("Enter words for password (separate by spaces)") if use_input_words else ""

st.title ("Results")
hide_password = st.checkbox("Hide password", value=False)
display_qr_code = st.checkbox("Display as QR code", value=False)

if st.button("Generate password"):
    if use_input_words and input_words:
        # Use the input words to create a password
        password = create_password_from_words(input_words)
        entropy = calculate_entropy(len(password))
    else:
        # Generate a random password
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
- Avoid using information that the user's colleagues and/or acquaintances might know to be associated with the user, such as relatives or pet names, romantic links (current or past), and biographical information (e.g. ID numbers, ancestors' names or dates).
- Do not use passwords that consist wholly of any simple combination of the aforementioned weak components.
""")
```

### Explanation of Changes:
1. **Checkbox `use_input_words`**: Adds an option for using input words.
2. **Text Input `input_words`**: Only visible if `use_input_words` is selected, where users can enter their own words.
3. **`create_password_from_words` Function**: Joins the words entered by the user into a single string to form the password.
4. **Conditional Password Generation**: Uses input words if `use_input_words` is checked; otherwise, it generates a random password.
