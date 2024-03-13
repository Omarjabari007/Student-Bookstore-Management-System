from inventory import Inventory
from shopping_cart import ShoppingCart
#Library system consist of the inventory of the book and the student partcipate in the library
class Library:
    def __init__(self):
        self.inventory = Inventory()
        self.students = {}  # Dictionary to store student IDs and their corresponding ShoppingCart instances
#Add a student to the library system
    def add_student(self, student_id, student_name):
        if student_id not in self.students:
            #We used the key as student id then it's values from the shopping cart (id , name , values(books)
            self.students[student_id] = ShoppingCart(student_id, student_name)  # Pass student_name to ShoppingCart
            print(f"Student: {student_name} --With-- ID: {student_id} added ... ")
        else:
            print(f"Student ---With--- ID: {student_id} already exist ... ")
#To show student already used the library or purchased from it
    def show_students(self):
        print("Students who used the library  : ")
        for student_id, shopping_cart in self.students.items():
            print(f"Student ID: {student_id}, Student Name: {shopping_cart.student_name}")

    def show_books_by_category_name(self , category):
        flag = False
        print(f"Books in the category: {category}")
        for item in self.inventory.books:
            if hasattr(item , 'category') and item.category == category:
                item.print_details()
                flag = True
        if not flag :
            print(f"Book with category: {category} is not exist in the inventory ... ")

    # this method to show students id with total spent in books
    def report(self):
        print("Sales Report:")
        for student_id, cart in self.students.items():
            total_spent = 0
            for item in cart.cart_items:
                book = item['book']
                quantity = item['quantity']
                item_total = book.price * quantity
                total_spent += item_total
            print(f"Student ID: {student_id} --> Total Spent: ${total_spent}")





