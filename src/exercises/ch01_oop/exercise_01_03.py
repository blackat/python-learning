class BankAccount:
    totalAccounts = 0

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        BankAccount.totalAccounts += 1

    def deposit(self, amount):
        self.balance = self.balance + amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")

        self.balance -= amount

    def get_balance(self):
        return self.balance

    def get_owner(self):
        return self.owner

    @classmethod
    def get_account_count(self):
        return self.totalAccounts

    def __str__(self):
        return f"BankAccount(owner={self.owner}, balance={self.balance})"
