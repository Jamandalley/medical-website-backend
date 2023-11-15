import re

def is_valid_email(email):
    # Define a regular expression pattern for the specific email pattern
    pattern = r'^\w+@\w+\.\w+$'

    # Use the re.match() function to check if the email matches the pattern
    if re.match(pattern, email):
        print("Email address matches pattern")
    else:
        print("Email address does not match pattern")

is_valid_email(input('Please enter a valid email address: '))

# Example usage:
# email_to_check = "jamiuabimbade@gmail.com"
# if is_valid_email(email_to_check):
#     print(f"{email_to_check} is a valid email address.")
# else:
#     print(f"{email_to_check} is not a valid email address.")
