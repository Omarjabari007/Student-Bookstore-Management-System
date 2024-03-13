
class ShoppingCart:
    def __init__(self, student_id, student_name):
        self.student_id = student_id
        self.student_name = student_name
        self.cart_items = []
        self.initial_money = 4000

    def add_to_cart(self, book, quantity):
        # Check if the quantity is allowed add the book with the quantity else print error
        if quantity > book.quantity:
            print(f"Error: Out of stock for {book.title} --> Available stock only : {book.quantity}")
            return False
        if self.initial_money < (book.price * quantity):
            print(f"Error: The purchase cannot be made due to lack of money $$ " )
            return False

        self.cart_items.append({"book": book, "quantity": quantity})
        print(f"Added quantity : {quantity}  of book : {book.title} to the shopping cart ..")

        # Decrease the quantity of the book in the inventory ................
        book.quantity -= quantity
        return True
    #To show the cart by the student id
    def view_cart(self):
        total_price = 0
        print(f"Shopping Cart for Student ID {self.student_id} name: {self.student_name}...")
        for item in self.cart_items:
            book = item['book']
            quantity = item['quantity']
            item_price = book.price * quantity
            total_price += item_price
            print(f"{book.title} by {book.author} --- Quantity: {quantity} --- Price: ${item_price}")
        print(f"Total Price: ${total_price}")
