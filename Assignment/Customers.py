class Customer:
    def __init__(self, id, companyname, contactname, address, phone):
        self.Id = id 
        self.CompanyName = companyname
        self.ContactName = contactname
        self.Address = address
        self.Phone = phone
    def __str__(self):
        return f"Customer(Id={self.Id}, Company='{self.CompanyName}', Contact='{self.ContactName}', Address='{self.Address}', Phone='{self.Phone}')"
   