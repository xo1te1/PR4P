from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = password

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publication_year": self.publication_year,
            "category_id": self.category_id
        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

def create_instances():
    db.create_all()

    if not Category.query.first():
        fiction = Category(name="Фантастика")
        non_fiction = Category(name="Наукова література")
        db.session.add_all([fiction, non_fiction])
        db.session.commit()

    if not Book.query.first():
        book1 = Book(title="Книга 1", author="Автор 1", publication_year=2025, category_id=1)
        book2 = Book(title="Книга 2", author="Автор 2", publication_year=2024, category_id=2)
        db.session.add_all([book1, book2])
        db.session.commit()

    if not User.query.first():
        user1 = User(name="Віка Кравчук", email="vika@gmail.com")
        user1.set_password("123456")
        user2 = User(name="Kate Igorivna", email="ivan@gmail.com")
        user2.set_password("qwerty")
        db.session.add_all([user1, user2])
        db.session.commit()

class UserList(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([user.serialize() for user in users])

    def post(self):
        data = request.json
        new_user = User(name=data['name'], email=data['email'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify(user.serialize())
        return {'message': 'User not found'}, 404

    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            data = request.json
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            if 'password' in data:
                user.set_password(data['password'])
            db.session.commit()
            return jsonify(user.serialize())
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted'}, 204
        return {'message': 'User not found'}, 404

class BookList(Resource):
    def get(self):
        books = Book.query.all()
        return jsonify([book.serialize() for book in books])

    def post(self):
        data = request.json
        new_book = Book(title=data['title'], author=data['author'], publication_year=data['publication_year'], category_id=data['category_id'])
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.serialize()), 201

class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get(book_id)
        if book:
            return jsonify(book.serialize())
        return {'message': 'Book not found'}, 404

    def put(self, book_id):
        book = Book.query.get(book_id)
        if book:
            data = request.json
            book.title = data.get('title', book.title)
            book.author = data.get('author', book.author)
            book.publication_year = data.get('publication_year', book.publication_year)
            book.category_id = data.get('category_id', book.category_id)
            db.session.commit()
            return jsonify(book.serialize())
        return {'message': 'Book not found'}, 404

    def delete(self, book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'message': 'Book deleted'}, 204
        return {'message': 'Book not found'}, 404

class CategoryList(Resource):
    def get(self):
        categories = Category.query.all()
        return jsonify([category.serialize() for category in categories])

    def post(self):
        data = request.json
        new_category = Category(name=data['name'])
        db.session.add(new_category)
        db.session.commit()
        return jsonify(new_category.serialize()), 201

class CategoryResource(Resource):
    def get(self, category_id):
        category = Category.query.get(category_id)
        if category:
            return jsonify(category.serialize())
        return {'message': 'Category not found'}, 404

    def put(self, category_id):
        category = Category.query.get(category_id)
        if category:
            data = request.json
            category.name = data.get('name', category.name)
            db.session.commit()
            return jsonify(category.serialize())
        return {'message': 'Category not found'}, 404

    def delete(self, category_id):
        category = Category.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return {'message': 'Category deleted'}, 204
        return {'message': 'Category not found'}, 404


api.add_resource(UserList, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(BookList, '/books')
api.add_resource(BookResource, '/books/<int:book_id>')
api.add_resource(CategoryList, '/categories')
api.add_resource(CategoryResource, '/categories/<int:category_id>')

if __name__ == '__main__':
    with app.app_context():
        create_instances()  # Додає початкові дані
    app.run(debug=True)