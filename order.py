from datetime import datetime
from shopping_cart import ShoppingCart
#we import the datetime to check the time of purchase
class Order:
    # I may change it to a big random id but for now the order id is a counter

    def __init__(self, cart):
        self.order_id = self.generate_order_id()
        self.cart = cart
        self.date = datetime.now()
    @staticmethod
    # To generate a unique order
    #static method belong to the class with the function to return unique id related to the time then hashes it to produce a unique identifier
    def generate_order_id():
        return abs(hash(datetime.now()))

#Print the order id and date of purchase
    def print_order_details(self):
        print(f"Order ID: {self.order_id}")
        print(f"Date of Purchase: {self.date}")
        print("Items Purchased:")
        for item in self.cart.cart_items:
            book = item['book']
            quantity = item['quantity']
            print(f"{book.title} by {book.author} --- Quantity: {quantity}")
        total_price = 0
        for item in self.cart.cart_items:
            book = item['book']
            quantity = item['quantity']
            total_price += book.price * quantity
        print(f"Total Price: ${total_price}")
