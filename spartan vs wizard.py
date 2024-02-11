import random


class Characters:
	def __init__(self,health,damage,speed):
		self.health = health
		self.damage = damage
		self.speed = speed
		


spartan = Characters(40,60,20)
wizard = Characters(85,60,30)

wizdam = wizard.damage
wizhea = wizard.health
spadam = spartan.damage
spahea = spartan.health

#print(spahea)


x = int(input("Toss, 0 OR 1, Wizard Chooses"))
y = random.randrange(1)
print(y)

while True:
	if x != y:
		print("Spartan wins the toss")
		print()
		print("Spartan Attqcks")
		if spadam >= wizhea:
			print("Spartan Attacks, wizard is defeated")
			break
		elif spadam < wizhea:
			print("Spartan Attacks, wizard blocks")
			print("Wizard attacks")
			if wizdam >= spahea:
				print("wizard attacks, spartan couldnt block it spartan is defeated")
				break
			
	else:
			print("Wizard wins the toss")
			print()
			print("Wizard attacks")
			if wizdam >= spahea:
				print("wizard attacks, spartan couldnt block it spartan is defeated")
				break
			elif wizdam<spahea:
				
				print("wizard attacks, spartan defends")
				print("Spartan Attqcks")
				if spadam >= wizhea:
					print("Spartan Attacks, wizard is defeated")
				break
			