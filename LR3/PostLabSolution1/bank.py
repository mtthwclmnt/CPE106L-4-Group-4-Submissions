#DYTIANQUIN, CHALZEA FRANSEN C.
from savingsaccount import SavingsAccount

class Bank:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def __str__(self):
        sorted_accounts = sorted(self.accounts)
        return "\n".join(str(account) for account in sorted_accounts)

    def test(self):
        # Create some test accounts
        self.add_account(SavingsAccount("Alice", 1500))
        self.add_account(SavingsAccount("Bob", 2000))
        self.add_account(SavingsAccount("Charlie", 2500))
        self.add_account(SavingsAccount("David", 3000))
        self.add_account(SavingsAccount("Ethan", 3500))

        # Print bank's accounts
        print(self)

if __name__ == "__main__":
    bank = Bank()
    bank.test()
