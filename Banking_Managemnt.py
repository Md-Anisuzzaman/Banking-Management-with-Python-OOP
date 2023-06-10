class Bank:
    def __init__(self):
        self.total_balance = 0
        self.total_loan_amount = 0
        self.loan_enabled = True
        self.loan_disabled = True
        self.accounts = []

    def create_account(self, name, initial_amount, role="user"):
        new_account = User(name, initial_amount, role)
        self.total_balance += initial_amount
        self.accounts.append(new_account)
        return new_account

    def update_total_balance(self, amount):
        self.total_balance += amount

    def update_total_loan(self, amount):
        self.total_loan_amount += amount
        self.total_balance -= amount


class User():
    def __init__(self, name, initial_amount, role="user"):
        self.name = name
        self.role = role
        self.loan_amount = 0
        self.deposit_amount = 0
        self.transfer_amount = 0
        self.withdrawn_amount = 0
        self.initial_amount = initial_amount
        self.balance = initial_amount
        self.transaction_history = []

    def balance_deposit(self, bank, amount):
        self.balance += amount
        self.deposit_amount += amount
        bank.update_total_balance(amount)
        new_transaction = {
            'transaction_type': "deposit",
            'amount': amount,
        }
        self.transaction_history.append(new_transaction)

    def balance_withdraw(self, bank, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.withdrawn_amount += amount
            bank.update_total_balance(-amount)
            new_transaction = {
                'transaction_type': "withdraw",
                'amount': amount,
            }
            self.transaction_history.append(new_transaction)
        else:
            print("Insufficient balance to perform this transaction.")

    def balance_transfer(self, recipient, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.transfer_amount += amount
            recipient.balance += amount

            new_transaction = {
                'transaction_type': "transfer",
                'recipient': recipient.name,
                'amount': amount,
            }
            self.transaction_history.append(new_transaction)
            transfer_to_recipient_transaction = {
                'transaction_type': "received",
                "From": self.name,
                "amount": amount
            }
            recipient.transaction_history.append(
                transfer_to_recipient_transaction)
        else:
            print("You have insufficient balance to perform the transfer.")

    def take_loan(self, bank, amount):
        condition_balance = self.balance * 2
        if condition_balance >= amount:
            self.balance += amount
            self.loan_amount += amount
            bank.update_total_loan(amount)
            transaction = {
                'transaction_type': 'loan',
                'amount': amount,
            }
            self.transaction_history.append(transaction)
        else:
            print("Loan Condition not fulfilled to take the loan")

    def check_balance(self):
        return self.balance

    def check_transaction_history(self):
        return self.transaction_history


class Admin:
    def __init__(self, bank):
        self.bank = bank

    def create_account(self, name, initial_amount, role):
        return self.bank.create_account(name, initial_amount, role)

    def get_total_balance(self):
        return self.bank.total_balance

    def get_total_loan_amount(self):
        return self.bank.total_loan_amount

    def enable_loan(self):
        self.bank.loan_enabled = True

    def disable_loan(self):
        self.bank.loan_enabled = False

    def get_loan_enabled(self):
        return self.bank.loan_enabled

    def get_loan_disabled(self):
        return self.bank.loan_disabled

    def get_all_accounts(self):
        all_accounts = []
        for account in self.bank.accounts:
            account_info = {
                'name': account.name,
                'balance': account.check_balance(),
                'loan_amount': account.loan_amount,
                'transaction_history': account.check_transaction_history()
            }
            all_accounts.append(account_info)
        return all_accounts


bank = Bank()
user_1 = bank.create_account("Ethian", 5000)
user_2 = bank.create_account("Juel", 2000)

admin = Admin(bank)
admin.create_account("Admin", 0, "admin")
# user_3 = bank.create_account("AMi admin", 0, "admin")

# deposit
user_1.balance_deposit(bank, 5000)
user_1.balance_deposit(bank, 5000)

# withdraw
user_1.balance_withdraw(bank, 1000)

# transfer
user_1.balance_transfer(user_2, 500)

# loan
user_1.take_loan(bank, 1000)

# Access the admin features
print("\nTotal Balance:", admin.get_total_balance())
print("Total Loan Amount:", admin.get_total_loan_amount())
print("Is Loan Enabled?", admin.get_loan_enabled())
print("Is Loan Disabled?", admin.get_loan_disabled())
# print("All Users:", admin.get_all_accounts())

# all_users = admin.get_all_accounts()
# for user in all_users:
#     print("Name:", user['name'])
#     print("Balance:", user['balance'])
#     print("Loan Amount:", user['loan_amount'])
#     print("Transaction History:")
#     for transaction in user['transaction_history']:
#         print(transaction)
#     print("-----------------------")




