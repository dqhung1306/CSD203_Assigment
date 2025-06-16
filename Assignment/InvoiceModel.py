from InvoiceAVLTree import AVLTree
from Database import Database
from Invoices import Invoice

class InvoiceModel:
    def __init__(self):
        self.tree = AVLTree()
        self.db = Database()
        self.loadInitialData()

    def loadInitialData(self):
        invoices = self.db.loadInvoices()
        for invoice in invoices:
            self.tree.insert(invoice)

    def countInvoices(self):
        return self.tree.countNodes(self.tree.root)
    
    def getTotalRevenue(self):
        return self.tree.getTotal(self.tree.root)
    
    def searchByCustomerID(self, customer_id):
        return self.tree.searchByCustomerID(customer_id)
    
    def searchByInvoiceID(self, invoice_id):
        return self.tree.searchByInvoiceID(invoice_id)