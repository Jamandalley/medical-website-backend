# import mysql.connector as sql
# mycon = sql.connect(host ='127.0.0.1', user ='root', passwd ='')
# mycursor = mycon.cursor()
# mycursor.execute("CREATE DATABASE recobank_db")
# mycon = sql.connect(host ='127.0.0.1', user ='root', password ='', database = 'recobank_db')
# mycursor = mycon.cursor()

# -- Create the Customers table to store customer information
# mycursor.execute("CREATE TABLE Customers(CustomerID VARCHAR(11) PRIMARY KEY, FirstName VARCHAR(255), LastName VARCHAR(255), DateOfBirth DATE, Email VARCHAR(255), Phone VARCHAR(20), Address VARCHAR(255))")


# -- Create the Accounts table to store information about customer accounts
# mycursor.execute("CREATE TABLE Accounts (AccountID VARCHAR(8) PRIMARY KEY, CustomerID  VARCHAR(11), AccountType VARCHAR(50), AccountNumber INT(10) UNIQUE, Balance  DECIMAL(15, 2), FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID))")

# -- Create the Transactions table to track account transactions
# mycursor.execute("CREATE TABLE Transactions (TransactionID VARCHAR(10) PRIMARY KEY, AccountID VARCHAR(8), TransactionDate DATETIME, Amount DECIMAL(15, 2), TransactionType VARCHAR(50), FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID))")

# -- Create a table for user authentication (simplified for demonstration)
# mycursor.execute("CREATE TABLE Users (UserID VARCHAR(10) PRIMARY KEY, Username VARCHAR(50) UNIQUE, PasswordHash VARCHAR(255), CustomerID VARCHAR(11), AccountNumber INT(10) UNIQUE, FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID))")

"""
FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID): This part defines a foreign key constraint. It states that the "CustomerID" column in the "Accounts" table is a foreign key that references the "CustomerID" column in the "Customers" table. This constraint enforces referential integrity, ensuring that the values in the "CustomerID" column of the "Accounts" table match values in the "CustomerID" column of the "Customers" table. In other words, it links accounts to specific customers based on their IDs.
"""

# -- Create indexes for improved query performance (optional)
# mycursor.execute("CREATE INDEX idx_CustomerID ON Accounts(CustomerID)")
# mycursor.execute("CREATE INDEX idx_AccountID ON Transactions(AccountID)")

"""CREATE INDEX idx_CustomerID: This part of the SQL query instructs the database to create an index with the name "idx_CustomerID." Indexes are database structures that improve the speed of data retrieval operations on specific columns in a table. In this case, the index is being created on the "CustomerID" column.

ON Accounts(CustomerID): This specifies that the index should be created on the "CustomerID" column of the "Accounts" table. In other words, it tells the database to create an index that helps optimize queries involving the "CustomerID" column in the "Accounts" table.

Creating an index on a column can significantly improve the performance of database queries that involve searching, sorting, or filtering by that column. It allows the database to quickly locate the relevant rows, making queries more efficient.
"""

# -- Add additional tables and fields as needed for stock trading and cryptocurrency features
# mycursor.execute("ALTER TABLE Customers ADD AccountNumber INT(10) NOT NULL UNIQUE")
# mycursor.execute("ALTER TABLE Transactions ADD AccountNumber INT(10) NOT NULL UNIQUE")
# mycursor.execute("ALTER TABLE Accounts ADD AccountNumber INT(10) UNIQUE")
# mycursor.execute("ALTER TABLE Users ADD AccountNumber INT(10) NOT NULL UNIQUE")
# myquery = "DELETE FROM Customers WHERE CustomerID = %s"
# val = 1
# mycursor.execute(myquery, val)

# mycursor.execute("ALTER TABLE Accounts DROP COLUMN AccountNumber")
# mycon.commit()
# mycon.close()
# mycursor.execute("DROP DATABASE recobank_db")