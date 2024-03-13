class Book:
    def __init__(self, title, author, price, quantity, category):
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity
        self.category = category
    def print_details(self):
        #To act as duck typing i will focus on behavior so to print details we gonna check if the necessary attributes are present
        #insted of focusing in the type of the object itself we gonna to focus on the behavior to print
        #to check if it has the needed attributes we can use build in function (hasattr)
        if hasattr(self,'title') and hasattr(self,'author') and hasattr(self,'price') and hasattr(self,'quantity') and hasattr(self,'category'):
            print(f"{self.title} by {self.author} --- Price: ${self.price} --- Stock: {self.quantity}")
        else:
            print("Invalid object to print the details_method  missing necessary attributes")
