from View.InvoiceView import Invoice_View
from Model.InvoiceModel import Invoice_Model

class Invoice_Controller:
    def __init__(self):
        self.model = Invoice_Model()
        self.view = Invoice_View()

    def run(self):
        while True:
            choice = self.view.displayMenu()
            try:
                if choice == '1':
                    total_revenue = self.model.getTotalRevenue()
                    self.view.displayTotalRevenue(total_revenue)
                elif choice == '2':
                    invoice_id = self.view.getInvoiceID()
                    invoice = self.model.searchByInvoiceID(invoice_id)
                    self.view.displayInvoice(invoice)
                elif choice == '3':
                    customer_id = self.view.getCustomerID()
                    invoices = self.model.searchByCustomerID(customer_id)
                    for invoice in invoices:
                        self.view.displayInvoice(invoice)
                elif choice == '4':
                    total_invoices = self.model.countInvoices()
                    self.view.displayTotalInvoices(total_invoices)
                elif choice == '5':
                    print("Exiting...")
                    break
                else:
                    self.view.displayError("Invalid choice")
            except ValueError as e:
                self.view.displayError(str(e))
            except Exception as e:
                self.view.displayError(f"Unexpected error: {str(e)}")

   