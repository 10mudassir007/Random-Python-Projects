class BankAccount:
    # creating a dictionary to store multiple accounts
    accounts = {}
    # initalizing with account number, balance and PIN CODE

    def __init__(self, ac_num, balance, pin):
        self.ac_num = ac_num
        self.pin = pin
        self.balance = balance

    # creating a function to desposit amount
    def deposit(self, amount):
        self.balance += amount

    # creating a function to withdraw amount
    def withdraw(self, amount):
        self.balance -= amount

    # creating a function to check balance
    def check_balance(self):
        print(self.balance)


# Using loop to keep creating accounts
while True:
    # Create account or exit
    create_account = int(input('Enter "0" to exit , "1" to create account : '))

    if create_account == 0:
        break

    elif create_account == 1:
        acn = int(input("Enter 4 digit account number : "))
        bal = 0
        pin = int(input("Enter 4 digit pin : "))
        account = BankAccount(acn, bal, pin)
        BankAccount.accounts[acn] = account
        print("Account Created with account number :", account.ac_num)

        # ACCOUNT CREATED

        # USING ANOTHER LOOP TO KEEP ASKING TO ACCESS ACCOUNT
        while True:
            access_account = int(
                input('Do you want to access your account "0" for NO and "1" for YES :')
            )

            if access_account == 1:
                # Prompt user for account number and pin
                enter_acn = int(input("Enter account number :"))
                enter_pin = int(
                    input(
                        "Enter pin :\nIf you enter wrong pin your account will be deactivated "
                    )
                )
                # Checking if an account with account number is created or not
                if enter_acn in BankAccount.accounts:
                    # Checking if the PIN entered is correct
                    if enter_pin == account.pin:
                        account = BankAccount.accounts[enter_acn]
                        # USING ANOTHER LOOP TO KEEP ASKING TO SELECT OPTIONS
                        while True:
                            options = int(
                                input(
                                    "1.Check Balance\n2.Deposit Amount\n3.Withdraw Amount\n0.EXIT "
                                )
                            )
                            # Checking balance
                            if options == 1:
                                print(f"Remaining Balance : {account.balance}")
                                continue
                            # Depositing amount
                            elif options == 2:
                                amount_to_deposit = int(
                                    input("Enter amount to deposit :")
                                )
                                account.deposit(amount_to_deposit)
                                print(
                                    f"Amount deposited, total balance is : {account.balance}"
                                )
                                continue
                            # Withdrawing amount
                            elif options == 3:
                                amount_to_withdraw = int(
                                    input("Enter amount to withdraw :")
                                )
                                account.withdraw(amount_to_withdraw)
                                print(
                                    f"Amount withdrawn, total balance is : {account.balance}"
                                )
                                continue
                            elif options == 0:
                                break
                            else:
                                print("Invalid Input")
                                break
                    else:
                        print("Invalid PIN \nYour account is deactivated")
                        break
                else:
                    print("Account not found")
                    break
            else:
                break

        recreate_account = int(
            input(
                'Enter "0" to exit or "1" to access existing accounts or "2" to create a new account : '
            )
        )
        if recreate_account == 0:
            continue
        elif recreate_account == 1:
            access_account2 = int(input("Enter account number : "))
            for account_number in BankAccount.accounts.keys():
                if account_number == access_account2:
                    pinAccount2 = int(input("Enter pin :"))
                    if pinAccount2 == BankAccount.accounts[access_account2].pin:
                        print(
                            f"Account Number: {account_number} \nBalance : {account.balance}"
                        )
                        options = int(
                            input(
                                "1.Check Balance\n2.Deposit Amount\n3.Withdraw Amount\n0.EXIT "
                            )
                        )
                        if options == 1:
                            print(f"Remaining Balance : {account.balance}")
                            break
                        elif options == 2:
                            amount_to_deposit = int(input("Enter amount to deposit :"))
                            account.deposit(amount_to_deposit)
                            print(
                                f"Amount deposited, total balance is : {account.balance}"
                            )
                            break
                        elif options == 3:
                            amount_to_withdraw = int(
                                input("Enter amount to withdraw :")
                            )
                            account.withdraw(amount_to_withdraw)
                            print(
                                f"Amount withdrawn, total balance is : {account.balance}"
                            )
                            break
                else:
                    print("Wrong PIN")
                    print(BankAccount.accounts[access_account2].pin)
                    break

            else:
                print("Account NOT FOUND")
                continue
    else:
        print("Invalid Input")
        break
