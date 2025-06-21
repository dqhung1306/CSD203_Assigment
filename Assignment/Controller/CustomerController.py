
from Model.CustomerModel import Customer_Model
from View.CustomerView import Customer_View

class Customer_Controller:
    def __init__(self):
        self.model = Customer_Model()
        self.view = Customer_View()

    def run(self):
        while True:
            choice = self.view.displayMenu()
            try:
                if choice == '1':
                    id, company_name, contact_name, address, phone = self.view.getCustomerInput()
                    self.model.addCustomer(id, company_name, contact_name, address, phone)
                    self.view.displaySuccess(f"Added customer {id}")
                elif choice == '2':
                    id = input("Enter Customer ID to search: ")
                    customer = self.model.searchCustomer(id)
                    self.view.displayCustomer(customer)
                elif choice == '3':
                    id = input("Enter Customer ID to update: ")
                    company_name, contact_name, address, phone = self.view.getUpdateInput()
                    self.model.updateCustomer(id, company_name, contact_name, address, phone)
                    self.view.displaySuccess(f"Updated customer {id}")
                elif choice == '4':
                    id = input("Enter Customer ID to delete: ")
                    self.model.deleteCustomer(id)
                    self.view.displaySuccess(f"Deleted customer {id}")
                elif choice == '5':
                    customers = self.model.getAllCustomers()
                    self.view.displayReport(customers)
                elif choice == '6':
                    total = self.model.getTotalCustomers()
                    self.view.displayTotal(total)
                elif choice == '7':
                    print("Exiting...")
                    break
                else:
                    self.view.displayError("Invalid choice")
            except ValueError as e:
                self.view.displayError(str(e))
            except Exception as e:
                self.view.displayError(f"Unexpected error: {str(e)}")