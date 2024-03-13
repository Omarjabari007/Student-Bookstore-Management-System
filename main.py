from book import Book
from library import Library
from shopping_cart import ShoppingCart
from order import Order
library = Library()
print(" Welcome to Classroom Of The Elite Library")
print("--------------------------------------------")

while True:
    print("1- Add Student")  # To add a student to the library database
    print("2- Add Book to Inventory")  # Add New Book to the storage
    print("3- View Inventory")  # To View the books in the storage
    print("4- Add Stock to Inventory")  # To increase the quantity of a specific book
    print("5- Add Book to Shopping Cart")  # To Add a specific book into your Shopping Cart
    print("6- Display Shopping Cart")  # To Display Your shopping cart
    print("7- Checkout")  # To print a receipt for the products sold to you
    print("8- Show Students")  # To Show the student in the Library DataBase
    print('9- Show Books By Category')  # to display all the books with a specific category
    print('10- Display The Reports')  # to show the total spent for every user id
    print("0- Exit")  # Exit the program ....

    choice = input("Enter your choice: ")

    if choice == '1':  # Create ur student (Std name , std id ) ...  and add it to the library database
        student_id = input("Enter student ID: ")
        student_name = input("Enter student name: ")
        library.add_student(student_id, student_name)

    elif choice == "2":  # Creating a book instance and add it to the inventory using library method add book  which in inventory
        title = input("Enter book title: ")
        author = input("Enter author: ")
        price = float(input("Enter price: "))
        quantity = int(input("Enter quantity: "))
        category = input("Enter category: ")
        book = Book(title, author, price, quantity, category)
        library.inventory.add_book(book)
        print(f"Book With Title: {title} added to the inventory ... ")

    elif choice == '3':  # Display the inventory using library class
        library.inventory.view_inventory()

    elif choice == '4':  # Add specific book into the library storage
        title = input("Enter book title to add stock: ")
        quantity = int(input("Enter quantity to add: "))
        library.inventory.add_stock(title, quantity)  # using library class

    elif choice == '5':
        student_id = input("Enter student ID: ")
        if student_id in library.students:
            cart = library.students[student_id]
            title = input("Enter book title to add to the shopping cart: ")
            quantity = int(input("Enter quantity: "))
            book = next((book for book in library.inventory.books if book.title == title), None)
            if book and quantity <= book.quantity:
                cart.add_to_cart(book, quantity)
            else:
                print("Book not found or insufficient stock.")
        else:
            print(f"Student with ID {student_id} not found.")

    elif choice == '6':
        student_id = input("Enter student ID to view shopping cart: ")
        if student_id in library.students:
            cart = library.students[student_id]
            cart.view_cart()
        else:
            print(f"Student with ID {student_id} not found.")

    elif choice == '7':
        student_id = input("Enter student ID to checkout: ")
        if student_id in library.students:
            cart = library.students[student_id]
            order = Order(cart)
            order.print_order_details()
        else:
            print(f"Student with ID {student_id} not found.")

    elif choice == '8':
        library.show_students()

    elif choice == '9':
        cat = input("Enter category name ... ")
        library.show_books_by_category_name(cat)

    elif choice == '10':
        print("Generating the reports ....")
        print("loading ...")
        library.report()

    elif choice == '0':
        print("Exiting the program.")
        break

    else:
        print("Invalid choice")
