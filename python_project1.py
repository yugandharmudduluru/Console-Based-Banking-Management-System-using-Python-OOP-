'''
conn	Connection to the database (bank.db)
conn.cursor()	Creates a cursor object to run SQL commands
cursor.execute()	Runs SQL queries
cursor.fetchone()	Gets one result from a SELECT query'''


import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()   #Create a cursor object from the database connection (conn) so you can execute SQL queries like SELECT, INSERT, UPDATE, or DELETE.

# Create accounts table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        acno TEXT PRIMARY KEY,
        name TEXT,
        balance REAL
    )
''')
conn.commit()     ## To save changes


class Bank:
    def add_account(self):
        name = input("Enter account holder name: ")
        acno = input("Enter account number: ")
        balance = float(input("Enter initial deposit amount: "))

        try:
            cursor.execute("INSERT INTO accounts (acno, name, balance) VALUES (?, ?, ?)",
                           (acno, name, balance))
            conn.commit()
            print(f"\n✅ Account created successfully for {name} (A/C No: {acno}) with ₹{balance:.2f} balance.\n")
        except sqlite3.IntegrityError:
            print("❌ Account number already exists.\n")

    def deposit(self):
        acno = input("Enter account number: ")
        amount = float(input("Enter amount to deposit: "))

        cursor.execute("SELECT balance FROM accounts WHERE acno = ?", (acno,))
        result = cursor.fetchone()
        if result:
            new_balance = result[0] + amount
            cursor.execute("UPDATE accounts SET balance = ? WHERE acno = ?", (new_balance, acno))
            conn.commit()
            print(f"✅ ₹{amount:.2f} deposited. Updated balance: ₹{new_balance:.2f}\n")
        else:
            print("❌ Account not found.\n")

    def withdraw(self):
        acno = input("Enter account number: ")
        amount = float(input("Enter amount to withdraw: "))

        cursor.execute("SELECT balance FROM accounts WHERE acno = ?", (acno,))
        result = cursor.fetchone()
        if result:
            balance = result[0]
            if amount > balance:
                print("❌ Insufficient balance!\n")
            else:
                new_balance = balance - amount
                cursor.execute("UPDATE accounts SET balance = ? WHERE acno = ?", (new_balance, acno))
                conn.commit()
                print(f"✅ ₹{amount:.2f} withdrawn. Remaining balance: ₹{new_balance:.2f}\n")
        else:
            print("❌ Account not found.\n")

    def display(self):
        acno = input("Enter account number: ")
        cursor.execute("SELECT name, acno, balance FROM accounts WHERE acno = ?", (acno,))
        result = cursor.fetchone()
        if result:
            print(f"📄 Account Summary\nName: {result[0]}\nAccount No: {result[1]}\nBalance: ₹{result[2]:.2f}\n")
        else:
            print("❌ Account not found.\n")


class HdfcBank(Bank):
    def rate_of_interest(self):
        acno = input("Enter account number: ")
        cursor.execute("SELECT name, balance FROM accounts WHERE acno = ?", (acno,))
        result = cursor.fetchone()
        if result:
            rate = 7  # 7% fixed interest
            interest = result[1] * rate / 100
            print(f"💹 Interest for {result[0]} at {rate}% is ₹{interest:.2f}\n")
        else:
            print("❌ Account not found.\n")


# 🔁 Menu-driven interface
hdfc = HdfcBank()

while True:
    print("1. Add Account\n2. Deposit\n3. Withdraw\n4. Display Account\n5. Calculate Interest\n6. Exit")
    choice = input("Choose an option: ")

    if choice == '1':
        hdfc.add_account()
    elif choice == '2':
        hdfc.deposit()
    elif choice == '3':
        hdfc.withdraw()
    elif choice == '4':
        hdfc.display()
    elif choice == '5':
        hdfc.rate_of_interest()
    elif choice == '6':
        print("👋 Exiting. Thank you for using HDFC Bank system.")
        break
    else:
        print("❌ Invalid option. Try again.\n")

# Close DB connection
conn.close()
