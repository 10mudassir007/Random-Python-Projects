class Hello:
	people = 0
	age_increase = 1
	def __init__(self,name,age):
		self.name = name
		self.age = age
		self.email = name + str(age) + "@email.com"
		Hello.people += 1
		
	def ageincrease(self):
		self.age = self.age  + Hello.age_increase
		
	@classmethod
	def increase_age(cls,increament):
		cls.age_increase = increament
	@classmethod	
	def from_str(cls,emp_string):
		name,age = emp_string.split("-")
		return cls(name,age)
	
	@staticmethod
	def statfunction(day):
		if day == 'sunday'.upper() or day == 'sunday':
			return False
		else:
			return True
	def __add__(self,other):
		return self.age + other.age
		
	def __repr__(self):
		return f"The Name of person is {self.name}"
		
	def __str__(self):
		return f"Employee({self.name},{self.age})"
		
if __name__ == ' __main__':
	j = Hello('John',20)
	k = Hello('Ken',30)
	print(j.email)
#j.ageincrease()

#print(j.age)
#j.increase_age(3)
#j.ageincrease()
#print(j.age)


#y = "Jon-65"
#x = Hello.from_str('John-5')
#print(Hello.from_str('Hello '))
#print(x.name,x.age)

#print(j.statfunction('sunday'))
#print(j.g)
#print(str(j))