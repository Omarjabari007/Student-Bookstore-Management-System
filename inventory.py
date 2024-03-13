# inventory.py
from book import Book

class Inventory:
    def __init__(self):
        self.books = []
#Add a book into the inventory (storage)
    def add_book(self, book):
        self.books.append(book)
#To display the books in the inventory by it's specific attributes for every book
    def view_inventory(self):
        for item in self.books:
            # checks if each item in the inventory has a print_details method and whether it's callable to work with duck typing
            #the hasattr  checks if the item object has an attribute named 'print_details' It returns True else return false
            if hasattr(item , 'print_details') and callable(getattr(item,'print_details',None)):
                #getattr(item , 'print_details' ,None) to get the print details attribute of 'item' if it exist it return the value else it's return None
                # callable it's check if the result is callable ... check if there are a print_details function !! methods and so ...
                item.print_details()
            else:
                print("Invalid object in inventory missed necessary attributes ! ")


#To increase the stock of specific book by title in the inventory
    def add_stock(self, title, quantity):
        #to add stock first we check if the book exist or no .......
        found = False
        for book in self.books:
            if book.title == title:
                book.quantity += quantity
                found = True
                print(f"Add {quantity} of book title {title} to the inventory")
                break

        if not found:
            print(f"Book title {title} not exist in the inventory")

