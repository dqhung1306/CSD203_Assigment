class Invoice :
    def __init__(self, id, customerid, products = {} , total = 0):
        self.InvoiceId = id
        self.CustomerId = customerid
        self.Products = products
        self.Total = total 
    def __str__(self):
        return f"InvoiceID: {self.InvoiceId}, CustomerID: {self.CustomerId}, Total: {self.Total}, Products: {self.Products}"

    