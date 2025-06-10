from AVLTree import AVLTree
from Database import Database
from Customers import Customer
import re

class CustomerModel:
    def __init__(self):
        self.tree = AVLTree()
        self.db = Database()
        self.loadInitialData()

    def loadInitialData(self):
        customers = self.db.loadCustomers()
        for customer in customers:
            self.tree.insert(customer)

    def validateCustomer(self, id, company_name, contact_name, address, phone):
        if not id or len(id) > 5:
            raise ValueError("Customer ID must be non-empty and up to 5 characters")
        if not company_name or len(company_name) > 40:
            raise ValueError("Company name must be non-empty and up to 40 characters")
        if not contact_name or len(contact_name) > 30:
            raise ValueError("Contact name must be non-empty and up to 30 characters")
        if not address or len(address) > 60:
            raise ValueError("Address must be non-empty and up to 60 characters")
        if not phone or not re.match(r'^\+?\d{10,15}$', phone):
            raise ValueError("Phone must be a valid number (10-15 digits)")

    def addCustomer(self, id, company_name, contact_name, address, phone):
        self.validateCustomer(id, company_name, contact_name, address, phone)
        customer = Customer(id, company_name, contact_name, address, phone)
        self.tree.insert(customer)
        self.db.addCustomer(customer)
        return customer

    def searchCustomer(self, id):
        node = self.tree.search(id)
        return node.data if node else None

    def updateCustomer(self, id, company_name=None, contact_name=None, address=None, phone=None):
        customer = self.searchCustomer(id)
        if not customer:
            raise ValueError("Customer not found")
        if company_name:
            self.validateCustomer(id, company_name, customer.ContactName, customer.Address, customer.Phone)
            customer.CompanyName = company_name
        if contact_name:
            self.validateCustomer(id, customer.CompanyName, contact_name, customer.Address, customer.Phone)
            customer.ContactName = contact_name
        if address:
            self.validateCustomer(id, customer.CompanyName, customer.ContactName, address, customer.Phone)
            customer.Address = address
        if phone:
            self.validateCustomer(id, customer.CompanyName, customer.ContactName, customer.Address, phone)
            customer.Phone = phone
        self.db.updateCustomer(customer)
        return customer

    def deleteCustomer(self, id):
        customer = self.searchCustomer(id)
        if not customer:
            raise ValueError("Customer not found")
        self.tree.delete(id)
        self.db.deleteCustomer(id)

    def getAllCustomers(self):
        result = []
        self.tree.inorderTraversal(self.tree.root, result)
        return result

    def getTotalCustomers(self):
        return self.tree.countNodes(self.tree.root)