import datetime

print('==============Age Calculator==============')

day = int(input('Enter day:'))
month = int(input('Enter month:'))
year = int(input('Enter year:'))

date_birth = datetime.datetime(day=day,month=month,year=year)

date_now = datetime.datetime.now()

age = (date_now.year - date_birth.year)

if (date_birth.month,date_birth.day) > (date_now.month,date_now.day):
    age -= 1

print(age)