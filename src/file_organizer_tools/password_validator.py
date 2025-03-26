import csv


def validator(username: str, password: str):
    if len(password) < 8:
        return False
    if username.lower() in password.lower():
        return False
    has_upper = any(character.isupper() for character in password)
    has_digit = any(character.isdigit() for character in password)
    has_special_char = any(character in '!#@$%^&*' for character in password)
    return has_upper and has_digit and has_special_char

def get_data(csv_file: str):
    with open(csv_file, newline='') as csvfile:
        reader_csv = csv.reader(csvfile)
        next(reader_csv)
        for file in reader_csv:
            result = validator(file[0],file[1])
            if result:
                print(f'Your password {file[1]} {file[0]} are secure')
            else:
                print(f'[¡] Your password {file[1]} {file[0]} is not secure')

        print(f'\nOperation Success !!!')

