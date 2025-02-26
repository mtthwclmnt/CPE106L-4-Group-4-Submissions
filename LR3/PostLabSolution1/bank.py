#DYTIANQUIN, CHALZEA FRANSEN C.
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

class SavingsAccount:
    def __init__(self, account_holder_name, balance=0):
        self.account_holder_name = account_holder_name
        self.balance = balance

    def __lt__(self, other):
        return self.account_holder_name < other.account_holder_name

    def __str__(self):
        return f"{self.account_holder_name}: ${self.balance:.2f}"


if __name__ == "__main__":
    bank = Bank()
    bank.test()
