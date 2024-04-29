import streamlit as st
import random
import string
import secrets
import pyqrcode
from PIL import Image


def get_random_string(length):
  """Generates a random string of lowercase letters of the given length.

  Args:
      length: The desired length of the random string.

  Returns:
      A random string consisting only of lowercase letters.
  """
  letters = string.ascii_lowercase
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str


def get_random_password(length):
  """Generates a random string of letters (lowercase and uppercase) and digits of the given length.

  Args:
      length: The desired length of the random string.

  Returns:
      A random string consisting of lowercase and uppercase letters and digits.
  """
  characters = string.ascii_letters + string.digits
  password = ''.join(random.choice(characters) for i in range(length))
  return password


def get_secure_random_string(length):
  """Generates a cryptographically secure random string of the given length.

  Args:
      length: The desired length of the random string.

  Returns:
      A cryptographically secure random string.
  """
  secure_str = ''.join((secrets.choice(string.ascii_letters) for i in range(length)))
  return secure_str


def get_random_alphanumeric_string(length):
  """Generates a random string consisting of letters and digits of the given length.

  Args:
      length: The desired length of the random string.

  Returns:
      A random string consisting of letters and digits.
  """
  source = string.ascii_letters + string.digits
  result_str = ''.join((random.choice(source) for i in range(length)))
  return result_str


def generate_qr_code(data):
  """Generates a QR code image from the given data.

  Args:
      data: The data to be encoded in the QR code.

  Returns:
      A PIL Image object containing the QR code.

  Raises:
      TypeError: If the data type is not supported for QR code encoding.
  """
  try:
      qr = pyqrcode.create(data)
      qr_image = qr.png(size=200)
      return qr_image
  except TypeError as e:
      # Handle data type error
      print(f"Error generating QR code: {e}")
      return None


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

# Generate
