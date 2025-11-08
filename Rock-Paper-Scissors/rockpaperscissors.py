# ROCK PAPER SCISSORS
import random

x = ""
while x != "q":
    choices = ["Rock", "Paper", "Scissors"]
    for i in enumerate(choices):
        print(f"{i[0] + 1}.{i[1]}")
    x = int(input("Enter choice: "))
    if x == 1:
        x = "Rock"
        choices.remove(x)
        comp = random.choice(choices)
        print(f"Player:{x}\nComp:{comp}")
        print(f"{x} vs {comp}")
        if comp == "Paper":
            print("Computer wins")
        else:
            print("Player wins")
    elif x == 2:
        x = "Paper"
        choices.remove(x)
        comp = random.choice(choices)
        print(f"Player:{x}\nComp:{comp}")
        print(f"{x} vs {comp}")
        if comp == "Scissors":
            print("Computer wins")
        else:
            print("Player wins")
    elif x == 3:
        x = "Scissors"
        choices.remove(x)
        comp = random.choice(choices)
        print(f"Player:{x}\nComp:{comp}\n")
        print(f"{x} vs {comp}\n")
        if comp == "Rock":
            print("Computer wins")
        else:
            print("Player wins")
    x = input("Press enter to play again or q to quit:")
