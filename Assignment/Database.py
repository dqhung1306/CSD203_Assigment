import pyodbc
from Customers import Customer

class Database:
    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LOQ;DATABASE=Northwind;Trusted_Connection=yes')
        self.cursor = self.conn.cursor()

    def loadCustomers(self):
        self.cursor.execute('SELECT CustomerID, CompanyName, ContactName, Address, Phone FROM Customers')
        return [Customer(row[0], row[1], row[2], row[3], row[4]) for row in self.cursor.fetchall()]

    def addCustomer(self, customer):
        query = "INSERT INTO Customers (CustomerID, CompanyName, ContactName, Address, Phone) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, (customer.Id, customer.CompanyName, customer.ContactName, customer.Address, customer.Phone))
        self.conn.commit()

    def updateCustomer(self, customer):
        query = "UPDATE Customers SET CompanyName = ?, ContactName = ?, Address = ?, Phone = ? WHERE CustomerID = ?"
        self.cursor.execute(query, (customer.CompanyName, customer.ContactName, customer.Address, customer.Phone, customer.Id))
        self.conn.commit()

    def deleteCustomer(self, id):
        query = "DELETE FROM Customers WHERE CustomerID = ?"
        self.cursor.execute(query, (id,))
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()