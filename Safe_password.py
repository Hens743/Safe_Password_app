import streamlit as st
import secrets
import string

def generate_password(length, include_letters=True, include_digits=True, include_punctuation=True, include_specials=False, include_scandinavian=False):
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

st.title("Secure Password Generator")

# Options for generating the password
length = st.number_input("Length of Password", min_value=1, value=8, step=1)
include_letters = st.checkbox("Include Letters", value=True)
include_digits = st.checkbox("Include Digits", value=True)
include_punctuation = st.checkbox("Include Punctuation", value=True)
include_specials = st.checkbox("Include Special Characters", value=False)
include_scandinavian = st.checkbox("Include Scandinavian Characters", value=False)
include_icelandic = st.checkbox("Include Icelandic Characters", value=False)

if st.button("Generate Password"):
    password = generate_password(length, include_letters, include_digits, include_punctuation, include_specials, include_scandinavian)
    if password:
        st.success(f"Generated Password: {password}")
