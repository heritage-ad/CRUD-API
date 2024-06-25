from flask import Flask, request 
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Interger, primary_key=True)
    book_name = db.Column(db.String(80),unique=True, nullable=False)
    author = db.Column(db.String(120))
    publisher = db.Column(db.String(150))

    def __repr__(self):
        return f"{self.name} - {self.description}"



@app.route('/')
def index():
    return 'Hello!'


@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_model = {'book_name' : book.name, 'author' : book.author, 'publisher' : book.publishe}
                      
        
        output.append(book_model)
    
    return {"books": output}


@app.route('/books/<id>')
def get_book(id):
    book= Book.query.get_or_404(id)
    return ({"book_name": book.name, "author": book.author, "publisher": book.publisher}) 

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['book_name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

@app.route('/books/<id>' , methods=['DELETE'])
def delete_book():
    book = Book.query.get(id)
    if book is None:
        return {"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "yeat!@"}