import random

capital_alphabets = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
lower_alphabets = [y.lower() for y in capital_alphabets]
numbers = ['0','1','2','3','4','5','6','7','8','9']
special_chars = ['!','@','#','$','%','&','?']

chars = capital_alphabets + lower_alphabets + numbers + special_chars
password = ''
for i in range(8):
    password += random.choice(chars)

print(password)