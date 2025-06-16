from CustomerController import CustomerController
from InvoiceController import InvoiceController
class MainController:
    def __init__(self):
        self.customer_controller = CustomerController()
        self.invoice_controller = InvoiceController()

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
    