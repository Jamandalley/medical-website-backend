import mysql.connector as sql
import datetime as dt
import hashlib
import random

class RECoBank:
    def __init__(self):
        self.conn = sql.connect(host ='127.0.0.1', user ='root', password ='', database = 'recobank_db')
        self.cursor = self.conn.cursor()             
        

    def create_customer(self):
        self.first_name = input("Enter customer's first name: ")
        self.first_name = self.first_name.strip().capitalize()
        self.last_name = input("Enter customer's last name: ")
        self.last_name = self.last_name.strip().capitalize()
        self.dob = input("Enter customer's date of birth (YYYY-MM-DD): ")
        self.email = input("Enter customer's email: ")
        
        # import re
        # self.pattern = r'^\w+@\w+\.\w+$'
        # if re.match(self.email, self.pattern):
        #     self.email = self.email.strip()
        #     return True

        # else:
        #     print("Please enter a valid email address")
        #     self.conn.rollback()
        #     self.create_customer()
        
        self.phone = input("Enter customer's phone number: ")
        self.address = input("Enter customer's address: ")
        self.address = self.address.strip()
        lower_case ="abcdefghijklmnopqrstuvwxyz"
        upper_case = "ABCDEFGHIJKLOMOPQRSTUVWXYZ"
        number = "0123456789"
        ID_sample = lower_case + upper_case + number
        length = 11
        customer_id ="".join(random.sample(ID_sample, length))
        self.customer_id = customer_id
        try:
            query = "INSERT INTO Customers (CustomerID, FirstName, LastName, DateOfBirth, Email, Phone, Address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            data = (self.customer_id, self.first_name, self.last_name, self.dob, self.email, self.phone, self.address)
            self.cursor.execute(query, data)
            self.conn.commit()
            self.conn.close()
            print(f"Customer {self.first_name} {self.last_name} added successfully with Customer ID ", {self.customer_id})
            # return self.cursor.lastrowid  # Return the customer ID
        
        except sql.Error as err:
            print(f"Error occured due to: {err}")
            self.conn.rollback()
            return None  

    def create_account(self):
        try:
            self.initial_balance = 0
            account_num = random.randint(4100000000, 4199999999)
            self.acct_num = account_num
            self.customer_id = input("Enter your customer ID: ")
            self.username = input("Set username: ")
            user_pwd = input("Set your user password: ")
            self.user_password = hashlib.sha256(user_pwd.encode()).hexdigest()
            self.username = self.username.strip().capitalize()
            # customer_id = self.customer_id.strip()
            # self.cust_id = customer_id
            acc_id = random.randint(10000000, 19999999)
            self.account_id = acc_id
            upper_case = "ABCDEFGHIJKLOMOPQRSTUVWXYZ"
            number = "0123456789"
            ID_sample = upper_case + number
            length = 10
            self.user_id = "".join(random.sample(ID_sample, length))
            self.acct_type = input("""Select your account type:
                              1. Savings
                              2. Current
                              
                              Your response (1/2): """)

            if self.acct_type == "1":
                self.account_type = "Savings"
            elif self.acct_type == "2":
                self.account_type = "Current"
            else:
                print("Please enter a valid response...")
                self.create_account()

            query1 = "INSERT INTO Accounts (AccountID, CustomerID, AccountType, AccountNumber, Balance) VALUES (%s, %s, %s, %s, %s)"
            data1 = (self.account_id, self.customer_id, self.account_type, self.acct_num, self.initial_balance)
            self.cursor.execute(query1, data1)
            self.conn.commit()
            query2 = "INSERT INTO Users (UserID, Username, PasswordHash, CustomerID, AccountNumber) VALUES (%s, %s, %s, %s, %s)"
            data2 = (self.user_id, self.username, self.user_password, self.customer_id, self.acct_num)
            self.cursor.execute(query2, data2)
            self.conn.commit()
            print(f"""Your account has been created successfully.
                      Your account details are:
                      Account number: {self.acct_num}
                      Account type: {self.account_type}
                      Initial balance: {self.initial_balance}
                      Account ID: {self.customer_id}
                      Username: {self.username}
                      userID: {self.user_id}
                      """)
        except sql.Error as err:
            print(f"Error: {err}")
            self.conn.rollback()


    def transfer(self, customer_id):
        self.customer_id = customer_id
        upper_case = "ABCDEFGHIJKLOMOPQRSTUVWXYZ"
        number = "0123456789"
        symbol = "!@#%&"
        ID_sample = upper_case + number + symbol
        length = 10
        self.trans_id = "".join(random.sample(ID_sample, length))
        try:
            account_number = int(input("Enter the recipient account number: "))
            self.account_number = account_number
            self.amount = float(input("Enter amount: "))

            # Fetch the initial balance
            query = "SELECT Balance FROM Accounts WHERE CustomerID = %s"
            val = (self.customer_id,)  
            self.cursor.execute(query, val)
            result = self.cursor.fetchone()
            
            # Check if the result is not None before attempting to access it
            if result is not None:
                init_bal = float(result[0])  
            
                # Calculate the new balance
            self.init_bal = init_bal
            new_bal = self.init_bal - self.amount
            if self.amount <= self.init_bal:
                self.new_bal = new_bal
                query1 = "UPDATE Accounts SET Balance =%s WHERE CustomerID = %s"
                data1 = (self.new_bal, self.customer_id)
                self.cursor.execute(query1, data1)
                query2 = "SELECT AccountID FROM Accounts WHERE CustomerID = %s"
                data2 = (self.customer_id,)
                self.cursor.execute(query2, data2)
                acct_id = self.cursor.fetchone()
                
                query3 = "INSERT INTO Transactions (TransactionID, AccountID, TransactionDate, Amount, TransactionType) VALUES (%s, %s, NOW(), %s, 'Transfer')"
                data3 = (self.trans_id, acct_id[0], self.amount)
                self.cursor.execute(query3, data3)
                self.conn.commit()
                print(f"${self.amount} has been transferred to {self.account_number} succesfully")
            elif self.amount > self.init_bal:
                print("Insufficient balance.")
                self.transfer(customer_id)

            
        except sql.Error as err:
            print(f"Error: {err}")
            self.conn.rollback()
            return False

    def withdraw(self, account_id, amount):
        try:
            query = "UPDATE Accounts SET Balance = Balance - %s WHERE AccountID = %s AND Balance >= %s"
            data = (amount, account_id, amount)
            self.cursor.execute(query, data)

            if self.cursor.rowcount == 0:
                return False  # Insufficient balance

            query = "INSERT INTO Transactions (AccountID, TransactionDate, Amount, TransactionType) VALUES (%s, NOW(), %s, 'Withdrawal')"
            data = (account_id, amount)
            self.cursor.execute(query, data)

            self.conn.commit()
            return True
        except sql.Error as err:
            print(f"Error: {err}")
            self.conn.rollback()
            return False

    def check_balance(self, account_id):
        try:
            query = "SELECT Balance FROM Accounts WHERE AccountID = %s"
            data = (account_id,)
            self.cursor.execute(query, data)
            result = self.cursor.fetchone()
            if result:
                print(f"Available balance: ${result[0]}")
            else:
                return None
        except sql.Error as err:
            print(f"Error: {err}")
            return None
    
    def authenticate_user(self, username, password):
        import hashlib
        self.username = username
        try:
            query = "SELECT CustomerID, PasswordHash FROM Users WHERE Username = %s"
            data = (self.username,)
            self.cursor.execute(query, data)
            result = self.cursor.fetchone()

            if result:
                customer_id, stored_password_hash = result
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                if password_hash == stored_password_hash:
                    return customer_id 
                
                else:
                    return None  # Authentication failed
            else:
                return None  # User not found
        except sql.Error as err:
            print(f"Error: {err}")
            return None
    
    def deposit(self, customer_id):
        try:
            self.customer_id = customer_id
            self.amount = float(input("Enter amount to deposit: "))
            upper_case = "ABCDEFGHIJKLOMOPQRSTUVWXYZ"
            number = "0123456789"
            symbol = "!@#%&"
            ID_sample = upper_case + number + symbol
            length = 10
            self.trans_id = "".join(random.sample(ID_sample, length))

            # Fetch the initial balance
            query = "SELECT Balance FROM Accounts WHERE CustomerID = %s"
            val = (self.customer_id,)  
            self.cursor.execute(query, val)
            result = self.cursor.fetchone()
            
            # Check if the result is not None before attempting to access it
            if result is not None:
                init_bal = float(result[0])
            
                # Calculate the new balance
                new_bal = init_bal + self.amount

                # Update the balance in the Accounts table
                query1 = "UPDATE Accounts SET Balance = %s WHERE CustomerID = %s"
                data1 = (new_bal, self.customer_id)
                self.cursor.execute(query1, data1)

                # Get the account ID
                query2 = "SELECT AccountID FROM Accounts WHERE CustomerID = %s"
                data2 = (self.customer_id,)
                self.cursor.execute(query2, data2)
                acct_id = self.cursor.fetchone()

                # Insert a transaction record
                query3 = "INSERT INTO Transactions (TransactionID, AccountID, TransactionDate, Amount, TransactionType) VALUES (%s, %s, NOW(), %s, 'Deposit')"
                data3 = (self.trans_id, acct_id[0], self.amount)
                self.cursor.execute(query3, data3)

                self.conn.commit()
                self.new_bal = new_bal
                print(f"${self.amount} deposited successfully.")
                print(f"Your new balance is ${self.new_bal}", "\n"*5)
                return True
            else:
                print("Customer not found.")
                return False
        except sql.Error as err:
            print(f"Error: {err}")
            self.conn.rollback()
            return False

    def check_transaction_history(self, customer_id):
        from prettytable import PrettyTable
        try:
            self.customer_id = customer_id

            # Retrieve the customer's transaction history
            query = """
                SELECT *
                FROM Transactions
                WHERE AccountID IN (
                    SELECT AccountID
                    FROM Accounts
                    WHERE CustomerID = %s
                )
                ORDER BY TransactionDate DESC
            """
            data = (self.customer_id,)
            self.cursor.execute(query, data)
            transaction_history = self.cursor.fetchall()

            if transaction_history:
                table = PrettyTable()
                table.field_names = ["TransactionID", "AccountID", "TransactionDate", "Amount", "TransactionType"]
                
                for row in transaction_history:
                    TransactionID, AccountID, TransactionDate, Amount, TransactionType = row	
                    table.add_row([TransactionID, AccountID, TransactionDate, Amount, TransactionType])
                # table.add_row(['TransactionID', 'AccountID', 'TransactionDate', 'Amount', 'TransactionType'])
                # print(transaction_history)
                print(table)
            else:
                print("No transaction history available for this customer.")
        except sql.Error as err:
            print(f"Error: {err}")

    
    def home_page(self, customer_id):
        query = "SELECT Balance FROM Accounts WHERE CustomerID = %s"
        val = (customer_id,) 
        self.cursor.execute(query, val)
        avail_bal = self.cursor.fetchone()
        avail_bal = avail_bal[0]
        print(f"""Your dashboard | Home page
              Available balance: ${avail_bal}
              
              1. Deposit                2. Withdrawal               3. Transfer
              
              4. Bill payment           5. Transaction history
              
              6. Log out
              """)
        self.user_resp = input("Enter reponse (1/2.../6): ")
        if self.user_resp == "1":
            self.deposit(customer_id)
        elif self.user_resp == "2":
            self.withdraw()
        elif self.user_resp == "3":
            self.transfer(customer_id)
        elif self.user_resp == "5":
            self.check_transaction_history(customer_id)
        else: 
            print("Services unavailable yet, please bear with us. Thanks for banking with us")

    def landing_page(self):
        try:
            while True:
                print("""             RECoBank Menu: 
                                1. Add Customer
                                2. Create account
                                3. Trasfer
                                4. Withdraw
                                5. Check Balance
                                6. Exit
                                7. Back
                                
                                """)

                choice = input("Enter your choice (1/2/3/4/5): ")

                if choice == "1":
                    bank.create_customer()
                elif choice == "2":
                    try:
                        print("""Are you a registered customer of RECoBank?: 
                                            1. Yes 
                                            2. No
                                            
                                            """)
                        user_resp = input("Enter your response(1/2): ")
                        if user_resp == "1":
                            bank.create_account()      
                        elif user_resp == "2":
                            inp = input("Press enter to continue or 1 to quit: ")
                            if inp != "1":
                                self.create_customer()
                                self.create_account()              
                            else:
                                self.landing_page()               
                            
                    except sql.Error as err:
                        print(f"Error: {err}")
                    
                elif choice == "3":
                    account_id = input("Enter account ID: ")
                    amount = float(input("Enter deposit amount: "))
                    success = bank.transfer(account_id, amount)
                    if success:
                        print(f"Deposited ${amount} into account {account_id}")
                    else:
                        print("Failed to deposit.")
                elif choice == "4":
                    account_id = input("Enter account ID: ")
                    amount = float(input("Enter withdrawal amount: "))
                    success = bank.withdraw(account_id, amount)
                    if success:
                        print(f"Withdrew ${amount} from account {account_id}")
                    else:
                        print("Failed to withdraw.")
                elif choice == "5":
                    account_id = input("Enter account ID: ")
                    balance = bank.check_balance(account_id)
                    if balance is not None:
                        print(f"Account balance: ${balance:.2f}")
                    else:
                        print("Account not found.")
                elif choice == "6":
                    print("Goodbye!")
                    break
                elif choice == "7":
                    bank.landing_page()
                else:
                    print("Invalid choice. Please choose a valid option.")
        finally:
            bank.close_connection()
    
    def close_connection(self):
        self.conn.close()

if __name__ == "__main__":
    bank = RECoBank()
    try:
        while True:
            print("""                       Welcome to RECoBank 
                            Menu:
                            1. Login
                            2. Home
                            3. Exit
                     """)

            choice = input("Enter your choice (1/2/3): ")

            if choice == "1":
                import time
                print("Please wait...")
                time.sleep(3)
                username = input("Enter your username: ")
                username = username.strip()
                password = input("Enter your password: ")
                customer_id = bank.authenticate_user(username, password)
                if customer_id:
                    print(f"Authentication successful. Welcome!")
                    # bank.landing_page()
                    bank.home_page(customer_id)
                    
                else:
                    print("Authentication failed. Please try again.")
            
            elif choice == "2":
                print("Please wait...")
                import time
                time.sleep(3)
                bank.landing_page()
                
            elif choice == "3":
                import time
                print("Please wait...")
                time.sleep(3)
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please choose a valid option.")
    finally:
        bank.close_connection()
