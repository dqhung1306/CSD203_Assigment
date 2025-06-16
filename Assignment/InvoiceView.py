class InvoiceView:
    def displayMenu(self):
        print("\n=== Invoice Management System ===")
        print("1. Total revenue")
        print("2. Search Invoice")
        print("3. Search Invoice by Customer ID")
        print("4. Total Invoices")
        print("5. Exit")
        return input("Enter your choice (1-5): ")
    
    def displayTotalRevenue(self, total):
        print(f"Total revenue: ${total:.2f}")
    
    def displayTotalInvoices(self, total):
        print(f"Total invoices: {total}")

    def getInvoiceID(self):
        return int(input("Enter Invoice ID to search: "))

    def displayInvoice(self, invoice):
        if invoice:
            print ( invoice )
        else:
            print("Invoice not found")
    def displayError(self, message):
        print(f"Error: {message}")
    def getCustomerID(self):
        return input("Enter Customer ID to search: ")
    def displayInvoices(self, invoices):    
        if invoices:
            for invoice in invoices:
                print ( invoice )
        else:
            print("No invoices found for this customer")