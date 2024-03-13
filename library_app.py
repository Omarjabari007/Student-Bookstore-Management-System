from flask import Flask, request, jsonify
import os
import uuid # to generate random ID
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields
from datetime import datetime
import json
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy # SQLALCHEMY import
#Database config
from flask_marshmallow import Marshmallow
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'library.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # database
ma = Marshmallow(app) # object of marshmellow

# creating the product models.....
class Student(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False) #  nullable : can't accept null value ... 
    cart = db.relationship('CartItem', backref='student', lazy=True) #  one to many relations for shoppingcart we can access specific students
# book model
class Book(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False) # nullable to be sure it can't be null 
    category = db.Column(db.String(50), nullable=False)
    orders = db.relationship('OrderItem', backref='book', lazy=True) # one to many relationship we can acess book from orders
    
#class StudentSchema(ma.SQLAlchemyAutoSchema):
  #  class Meta:
   #     model = Student
#OrderItem model 
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), db.ForeignKey('order.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
#Order model
class Order(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    items = db.relationship('OrderItem', backref='order', lazy=True)
# for every OrderItem object will created an Order also will created due to the relationShip between them in the database
#CartItem model 
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('student.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False) #Foreignkey book.id 
    quantity = db.Column(db.Integer, nullable=False)
#test...
with app.app_context():
    db.create_all()

#/add_book to add a book (everything will be in the photos file  to show the results)
@app.route('/add_book', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        author=data['author'],
        price=data['price'],
        quantity=data['quantity'],
        category=data['category']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201 
#/get_books to retrive  the books from the database
@app.route('/get_books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_data = {
            'title': book.title,
            'author': book.author,
            'price': book.price,
            'quantity': book.quantity,
            'category': book.category
        }
        book_list.append(book_data)
    return jsonify({'books': book_list})
# /add_student to add a new student and put it in the database
@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        new_student = Student(id=data['id'], name=data['name'])
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'message': 'Student added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#  /delete_student/4  Delete student by ID here delete std 4 for example 
@app.route('/delete_student/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        student = Student.query.get(student_id)

        if student:
            db.session.delete(student) #delete ..
            db.session.commit()
            return jsonify({'message': f'Student with ID {student_id} deleted successfully'}), 200
        else:
            return jsonify({'message': f'Student with ID {student_id} not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get all students
#/get_students to retrive all the students from the database .. show it in the web 
@app.route('/get_students', methods=['GET'])
def get_students():
    students = Student.query.all()

    student_list = []
    for student in students:
        student_data = {
            'id': student.id,
            'name': student.name,
        }
        student_list.append(student_data)

    # Return the manually serialized data as JSON response
    return jsonify({'students': student_list})

# now to add items to cart 
#cart handling
#/add_to_cart every std id related to specific cart we add books to this cart 
@app.route('/add_to_cart' , methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        std_id = data.get('student_id')
        book_id = data.get('book_id')
        quantity = data.get('quantity' , 3 )  # 3 quantity if the quantity is not provided ... .
        book = Book.query.get(book_id) # check if the book is already exist 
        student = Student.query.get(std_id)
        if not student or not book:
            return jsonify({'error' : 'Book or Student not found'}) , 404
        
        cart_item = CartItem.query.filter_by(student_id=std_id, book_id=book_id).first()
        if book.quantity < quantity:
            return jsonify({'error': 'No enough Stock'}), 400
        
        book.quantity -= quantity
        order = Order(id=str(uuid.uuid4()), date=datetime.now()) #generate random ID 
        db.session.add(order)
        order_item = OrderItem(order_id=order.id, book_id=book_id, quantity=quantity)
        db.session.add(order_item)
        #every Std related with his cart OrderItem and everyone is connected with the order


        if cart_item:
        # Book is already in the cart
        
            cart_item.quantity += quantity
        else:
        # Book is not in the cart so  add a new cart item
            new_cart_item = CartItem(student_id=std_id,
                                     book_id=book_id,
                                     quantity=quantity
                                     )
            db.session.add(new_cart_item)
        db.session.commit()
        return jsonify({'message' : 'Book added to the cart'}), 201
    except Exception as e:
        return jsonify({'error' : str(e)}) , 500
    
    
#/get_cart_items/1   get specific cart with it's value for specific id number ,, here std number 1 for example
@app.route('/get_cart_items/<string:student_id>' , methods =['GET'])
def get_cart_items(student_id):
    try:
        student = Student.query.get(student_id)

        if not student:
            return jsonify({'error': 'Student not found in the Student list '}), 404
        cart_items = CartItem.query.filter_by(student_id=student_id).all()

        cart_list = []
        for cart_item in cart_items:
            book = Book.query.get(cart_item.book_id)
            cart_data = {
                'book_id': cart_item.book_id,
                'title': book.title,
                'quantity': cart_item.quantity,
            }
            cart_list.append(cart_data)

        return jsonify({'cart_items': cart_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
                   

        
if __name__ == '__main__':
    app.run(debug=True)
