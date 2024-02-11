def calc_age(birth_year,curr_year):
	return curr_year-birth_year
	
x = int(input("Enter current year"))
y = int(input("Enter birth year"))

print(f"you are {calc_age(y,x)} years old")
