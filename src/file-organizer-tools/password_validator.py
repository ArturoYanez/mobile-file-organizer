def validator(username: str, password: str):
    if len(password) < 8:
        return False
    if username.lower() in password.lower():
        return False
    has_upper = any(character.isupper() for character in password)
    has_digit = any(character.isdigit() for character in password)
    has_special_char = any(character in '!#@$%^&*' for character in password)
    return has_upper and has_digit and has_special_char

print(validator('angel', 'Manuel*732828272'))

