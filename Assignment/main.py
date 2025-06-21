from Controller.CustomerController import Customer_Controller
from Controller.InvoiceController import Invoice_Controller
class MainController:
    def __init__(self):
        self.customer_controller = Customer_Controller()
        self.invoice_controller = Invoice_Controller()

    def run(self):
        while True:
            print("Main Menu:")
            print("1. Customer Management")
            print("2. Invoice Management")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.customer_controller.run()
            elif choice == '2':
                self.invoice_controller.run()
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice, please try again.")
if __name__ == "__main__":
    controller = MainController()
    controller.run()
    