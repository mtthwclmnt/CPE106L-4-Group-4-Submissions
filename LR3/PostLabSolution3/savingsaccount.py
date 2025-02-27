#DYTIANQUIN, CHALZEA FRANSEN C.
class SavingsAccount:
    def __init__(self, account_holder_name, balance=0):
        self.account_holder_name = account_holder_name
        self.balance = balance

    def __lt__(self, other):
        return self.account_holder_name < other.account_holder_name

    def __str__(self):
        return f"{self.account_holder_name}: ${self.balance:.2f}"
