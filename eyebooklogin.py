print("EYEBOOK")
print('Begin by creating account:')
print()





data = {}
def create():	
	print('Eyebook create account')
	print()
	data['a'] = input('Enter Username:')
	print()
	data['b'] = input('Enter Email or Phone Number:')
	print()
	data['c'] = input('Enter Password:')
	print()

def eye_book():
	x = int(input("Create Account by entering 0, sign in by entering 1"))
	if x == 0:
		create()
		y = input("Sign In ?, Y/N")
		if y == "Y" or "y":
			
			m = data['a']
			n = data['b']
			o = data['c']
	
			print()
			print('EYEBOOK')
			print()
			print('Welcome to Eyebook.com')
			print()
			print('Enter your login details')
			print()


			x = str(input('Enter your username:'))
			print()
			X=input("Enter your email or phone number: ")
			print()
			y = str(input('Enter your password'))
			print()
	
			if   x == m and X == n and y == o:
				print('Sign in,')
				z = input('Y for Yes , N for No')
				if z == "Y " or "y":
					print('Sign in successful')
				else:
					print('not signed in')
			elif True:
				while x != m and X != n and y != o:
					print('NotSigned In')
					print()
					n=input("Retry, Y/N")
					if n == "Y" or "y":
						x = str(input('Enter your username'))
						print()
						X = input("Enter your email or phone number")
						print()
						y = str(input('Enter your password'))
						print()
							
				
			
		else:
			print("Please recheck your credentials")



eye_book()