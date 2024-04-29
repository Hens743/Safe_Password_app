### 1-Generating random strings ###

# Example to generate a random string of any length

import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)

get_random_string(8)
get_random_string(6)
get_random_string(4)

# Random String of Lower Case and Upper Case Letters

def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    # print random string
    print(result_str)

# string of length 8
get_random_string(8)
get_random_string(8)

# Random string of specific letters
# Random string of length 5
result_str = ''.join((random.choice('abcdxyzpqr') for i in range(5)))
print(result_str)

# Random String without Repeating Characters

for i in range(3):
    # get random string of length 6 without repeating letters
    result_str = ''.join(random.sample(string.ascii_lowercase, 8))
    print(result_str)
    
# Create Random Password with Special characters, letters, and digits

# get random password pf length 8 with letters, digits, and symbols
characters = string.ascii_letters + string.digits + string.punctuation
password = ''.join(random.choice(characters) for i in range(8))
print("Random password is:", password)

  # Using the string.printable

password = ''.join(random.choice(string.printable) for i in range(8))
print("Random password is:", password)

#Random password with a fixed count of letters, digits, and symbols
import random
import string

def get_random_password():
    random_source = string.ascii_letters + string.digits + string.punctuation
    # select 1 lowercase
    password = random.choice(string.ascii_lowercase)
    # select 1 uppercase
    password += random.choice(string.ascii_uppercase)
    # select 1 digit
    password += random.choice(string.digits)
    # select 1 special symbol
    password += random.choice(string.punctuation)

    # generate other characters
    for i in range(6):
        password += random.choice(random_source)

    password_list = list(password)
    # shuffle all characters
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password

print("First Random Password is ", get_random_password())
# output  qX49}]Ru!(
print("Second Random Password is ", get_random_password())
# Output  3nI0.V#[T

# Generate a secure random string and password

import secrets
import string

# secure random string
secure_str = ''.join((secrets.choice(string.ascii_letters) for i in range(8)))
print(secure_str)
# Output QQkABLyK

# secure password
password = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(8)))
print(password)
# output 4x]>@;4)

# Generate a random alphanumeric string of letters and digits

# get random string of letters and digits
source = string.ascii_letters + string.digits
result_str = ''.join((random.choice(source) for i in range(8)))
print(result_str)
# Output vZkOkL97

# Random alphanumeric string with a fixed count of letters and digits

import random
import string

def get_string(letters_count, digits_count):
    letters = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
    digits = ''.join((random.choice(string.digits) for i in range(digits_count)))

    # Convert resultant string to list and shuffle it to mix letters and digits
    sample_list = list(letters + digits)
    random.shuffle(sample_list)
    # convert list to string
    final_string = ''.join(sample_list)
    print('Random string with', letters_count, 'letters', 'and', digits_count, 'digits', 'is:', final_string)

get_string(5, 3)
# Output get_string(5, 3)

get_string(6, 2)
# Output Random string with 6 letters and 2 digits is: 7DeOCm5t

# Generate a random string token
import secrets
print("Secure hexadecimal string token", secrets.token_hex(32))

### Generate universally unique secure random string Id

The random string generated using a UUID module is suitable for the Cryptographically secure application. The UUID module has various functions to do this. Here in this example, we are using a uuid4() function to generate a random string Id.

import uuid
stringId  = uuid.uuid4()
print("Secure unique string id", stringId)

# Use the StringGenerator module to generate a random string
    pip install StringGenerator.
    Use a render() function of StringGenerator to generate randomized strings of characters using a template
  
 import strgen

random_str = strgen.StringGenerator("[\w\d]{10}").render()
print(random_str)
# Output 4VX1yInC9S

random_str2 = strgen.StringGenerator("[\d]{3}&[\w]{3}&[\p]{2}").render()
print(random_str2)
# output "C01N=10
# Output 0682042d-318e-45bf-8a16-6cc763dc8806

### 2 Pure python QR Code generator ###
pip install qrcode

import qrcode
img = qrcode.make('Some data here')
type(img)  # qrcode.image.pil.PilImage
img.save("some_file.png")

import qrcode
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data('Some data')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

OR

import qrcode
from qrcode.image.pure import PyPNGImage
img = qrcode.make('Some data here', image_factory=PyPNGImage)
