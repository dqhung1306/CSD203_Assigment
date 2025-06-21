class Customer_View:
    def displayMenu(self):
        print("\n=== Customer Management System ===")
        print("1. Add Customer")
        print("2. Search Customer")
        print("3. Update Customer")
        print("4. Delete Customer")
        print("5. Generate Customer Report")
        print("6. Total Customers")
        print("7. Exit")
        return input("Enter your choice (1-7): ")

    def getCustomerInput(self):
        id = input("Enter Customer ID (max 5 chars): ")
        company_name = input("Enter Company Name: ")
        contact_name = input("Enter Contact Name: ")
        address = input("Enter Address: ")
        phone = input("Enter Phone Number: ")
        return id, company_name, contact_name, address, phone

    def getUpdateInput(self):
        print("Enter new values (leave blank to keep unchanged):")
        company_name = input("New Company Name: ") or None
        contact_name = input("New Contact Name: ") or None
        address = input("New Address: ") or None
        phone = input("New Phone Number: ") or None
        return company_name, contact_name, address, phone

    def displayCustomer(self, customer):
        if customer:
            print(customer)
        else:
            print("Customer not found")

    def displayReport(self, customers):
        if not customers:
            print("No customers in the system")
        else:
            print("\nCustomer Report:")
            for customer in customers:
                print(customer)

    def displayTotal(self, total):
        print(f"Total customers: {total}")

    def displayError(self, message):
        print(f"Error: {message}")

    def displaySuccess(self, message):
        print(f"Success: {message}")