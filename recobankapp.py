
import time
import sys
import mysql.connector as sql
class Bank:
    def __init__(self):
        self.name = 'Bank'
        # self.acct_number = acct_number
        self.landing_page()
    
    def quick_balance(self):
        print('Press enter to continue or 1 to quit')
        self.response_2 = input('Your response: ')
        print('Please wait...')
        time.sleep(3)
        if self.response_2 != '1':
            self.user_acct = input('Enter your account number: ')
            self.password = input('Enter your password: ')
            try:
                self.acct = self.user_acct.strip()
                self.password = self.password.strip()
                mycon = sql.connect(host ='127.0.0.1', user ='root', passwd ='', database = 'recobank_db')
                mycursor = mycon.cursor()
                myquery = "SELECT * FROM customer_profile WHERE account_number =%s AND password = %s"
                val = (self.acct, self.password)
                mycursor.execute(myquery, val)
                self.user_details = mycursor.fetchall()
            
                if self.user_details:
                    myquery = "SELECT account_balance, account_type FROM trasaction_records WHERE account_number =%s"
                    val = (self.acct)
                    mycursor.execute(myquery, val)
                    output = mycursor.fetchall()
                    for results in output:
                        print(f"{results} '\n', {self.acct}")
                    mycon.close()
                else:
                    print('Please sign up with the bank...')
            except TypeError:
                print("Please enter a valid account number...")
            except Exception as e:
                print("Error occured due to: " + str(e))
        else:
            print("Thank you for banking with us...")
            self.landing_page()
                
    def quick_transfer(self):
        self.login()
        print("""  Warning: Quick Transfer Transaction Limit: #20,000
                        Cumulative Daily Limit: #50,000
                            Please select the Transfer Type
                        1. Transfer to other Banks
                        2. Transfer to RECoBank account
                        3. Exit
              """)
        self.user_resp = input('Your response: ')
        print("Please wait...")
        time.sleep(3)
        try:
            if self.user_resp.strip() == "1":
                print("""                       Please select the bank:
                                    1. Access bank
                                    2. GTBank
                                    3. Diamond Bank
                                    4. Kuda Microfinance Bank
                                    5. Moniepoint Microfinance Bank
                                    6. Opay Microfinance Bank
                                    7. Zenith Bank
                                    8. United Bank for Africa
                                    9. Polaris Bank
                                    10. Union Bank
                                    
                      """)
                self.user_inp = input("Response: ")
                time.sleep(2)
                if self.user_inp == range(1, 10):
                    self.user_inp2 = int(input("Please enter the recepients account number: "))
                    self.user_inp3 = float(input("Please enter the amount you wish to transfer: "))
                    print("Please wait... ")
                    time.sleep(3)
                    # user_inp2 = user_inp2.strip()
                    # user_inp3 = user_inp3.strip()
                    self.user_pswd = input("Please enter your transaction pasword: ")
                    self.user_pswd = self.user_pswd.strip()
                    mycon = sql.connect(host ='127.0.0.1', user ='root', passwd ='', database = 'recobank_db')
                    mycursor = mycon.cursor()
                    myquery_acctnum = "SELECT account_number FROM customer_profile WHERE password = %s"
                    val = (self.user_pswd)
                    mycursor.execute(myquery_acctnum, val)
                    acctnum = mycursor.fetchall()[0]
                    self.acct = mycursor.execute("SELECT account_balance FROM trasaction_records WHERE account_number = %s")
                    val = (acctnum)
                    mycursor.execute(self.acct, val)
                    init_bal = mycursor.fetchall()[0]
                    final_bal = f"{init_bal} - {self.user_inp3}"
                    upd_query = "UPDATE transaction_records SET account_balance =%s WHERE account_number = %s"
                    upd_val = (final_bal, acctnum)
                    mycursor.execute(upd_query, upd_val)
                    
                    self.user_details = mycursor.fetchall()[0]
                    if self.user_details:
                        my_query = mycursor.execute("SELECT account_balance FROM trasaction_records WHERE account_number = %s")
                        val = (self.)
                        
                
                
                
    
    def login(self):
        self.user_email = input("Enter your email address: ")
        self.user_paswd = input("Enter your password: ")
        try: 
            import re
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(self.user_email, pattern):
                self.user_paswd = self.user_paswd.strip()
                mycon = sql.connect(host ='127.0.0.1', user ='root', passwd ='', database = 'recobank_db')
                mycursor = mycon.cursor()
                myquery = "SELECT * FROM customer_profile WHERE user_email=%s AND password = %s"
                val = (self.user_email, self.user_paswd)
                mycursor.execute(myquery, val)
                self.user_details = mycursor.fetchall()
                mycon.close()
                if self.user_details:
                    self.landing_page()
            else:
                print("Invalid username or password	")
                self.login()
        except NameError:
            print("Please enter a valid email address")
        except TypeError:
            print("Invalid email address or password")
        except Exception as e:
            print("Error occurred due to: ", str(e))
            self.login()
            
    
    def landing_page(self):
        print('''                       WELCOME TO RECoBank!!!
                        Please select the operation you want to perform:
                        1. Quick balance
                        2. Quick transfer
                        3. Quick airtime 
                        4. Soft token
                        5. Account manager
                        6. Open account
                        
              ''')
        response_1 = input('Your response: ').strip()
        if response_1 == '1':
            self.quick_balance()
        if response_1 == '2':
            self.quick_transfer()       


import random

class Customer:
    def __init__(self, name, balance=0.0):
        self.name = name
        self.balance = balance
        self.account_number = random.randint(1000, 9999)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited ${amount}. New balance: ${self.balance}"
        else:
            return "Invalid deposit amount."

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return f"Withdrew ${amount}. New balance: ${self.balance}"
        else:
            return "Insufficient funds or invalid withdrawal amount."

    def get_balance(self):
        return f"Account Balance for {self.name}: ${self.balance}"

class Bank:
    def __init__(self, name):
        self.name = name
        self.customers = {}

    def add_customer(self, name):
        if name not in self.customers:
            customer = Customer(name)
            self.customers[name] = customer
            return f"Customer {name} added to {self.name}."
        else:
            return f"Customer {name} already exists in {self.name}."

    def get_customer(self, name):
        if name in self.customers:
            return self.customers[name]
        else:
            return f"Customer {name} not found in {self.name}."

    def __str__(self):
        return f"Bank: {self.name}\nCustomers: {', '.join(self.customers.keys())}"


if __name__ == "__main__":
    reco_bank = Bank("RECoBank")
    while True:
        print("\nRECoBank Menu:")
        print("1. Add Customer")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == "1":
            customer_name = input("Enter customer name: ")
            print(reco_bank.add_customer(customer_name))
        elif choice == "2":
            customer_name = input("Enter customer name: ")
            amount = float(input("Enter deposit amount: "))
            customer = reco_bank.get_customer(customer_name)
            print(customer.deposit(amount))
        elif choice == "3":
            customer_name = input("Enter customer name: ")
            amount = float(input("Enter withdrawal amount: "))
            customer = reco_bank.get_customer(customer_name)
            print(customer.withdraw(amount))
        elif choice == "4":
            customer_name = input("Enter customer name: ")
            customer = reco_bank.get_customer(customer_name)
            print(customer.get_balance())
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")


import mysql.connector

# Database connection parameters
db_config = {
    "host": "your_database_host",
    "user": "your_database_user",
    "password": "your_database_password",
    "database": "your_database_name"
}

class RECoBank:
    def __init__(self):
        self.conn = mysql.connector.connect(**db_config)
        self.cursor = self.conn.cursor()

    # ... Define your RECoBank class methods for customer, account, deposit, withdraw, check_balance, etc.

    def close_connection(self):
        self.conn.close()

if __name__ == "__main__":
    bank = RECoBank()
    try:
        while True:
            print("\nRECoBank Menu:")
            print("1. Add Customer")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Check Balance")
            print("5. Exit")

            choice = input("Enter your choice (1/2/3/4/5): ")

            if choice == "1":
                first_name = input("Enter customer's first name: ")
                last_name = input("Enter customer's last name: ")
                dob = input("Enter customer's date of birth (YYYY-MM-DD): ")
                email = input("Enter customer's email: ")
                phone = input("Enter customer's phone number: ")
                address = input("Enter customer's address: ")
                customer_id = bank.create_customer(first_name, last_name, dob, email, phone, address)
                if customer_id:
                    print(f"Customer {first_name} {last_name} added with ID: {customer_id}")
            elif choice == "2":
                account_id = input("Enter account ID: ")
                amount = float(input("Enter deposit amount: "))
                success = bank.deposit(account_id, amount)
                if success:
                    print(f"Deposited ${amount} into account {account_id}")
                else:
                    print("Failed to deposit.")
            elif choice == "3":
                account_id = input("Enter account ID: ")
                amount = float(input("Enter withdrawal amount: "))
                success = bank.withdraw(account_id, amount)
                if success:
                    print(f"Withdrew ${amount} from account {account_id}")
                else:
                    print("Failed to withdraw.")
            elif choice == "4":
                account_id = input("Enter account ID: ")
                balance = bank.check_balance(account_id)
                if balance is not None:
                    print(f"Account balance: ${balance:.2f}")
                else:
                    print("Account not found.")
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please choose a valid option.")
    finally:
        bank.close_connection()


