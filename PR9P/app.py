from flask import Flask, request, Response
import json

app = Flask(__name__)

books = [
    {"id": 1, "title": "Кобзар", "author": "Тарас Шевченко", "year": 1840},
    {"id": 2, "title": "Тіні забутих предків", "author": "Михайло Коцюбинський", "year": 1911},
    {"id": 3, "title": "Захар Беркут", "author": "Іван Франко", "year": 1883}
]

def json_response(data, status=200):
    return Response(
        response=json.dumps(data, ensure_ascii=False, indent=2),
        status=status,
        mimetype="application/json"
    )

@app.route("/books", methods=["GET"])
def get_books():
    return json_response(books)

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return json_response(book)
    return json_response({"message": "Книгу не знайдено"}, 404)

@app.route("/books", methods=["POST"])
def add_book():
    new_book = request.json
    if not all(k in new_book for k in ("id", "title", "author", "year")):
        return json_response({"message": "Невірний формат даних"}, 400)

    if any(b["id"] == new_book["id"] for b in books):
        return json_response({"message": "Книга з таким ID вже існує"}, 400)

    books.append(new_book)
    return json_response({"message": "Книгу додано", "book": new_book}, 201)

@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return json_response({"message": "Книгу не знайдено"}, 404)

    update_data = request.json
    book.update(update_data)
    return json_response({"message": "Книгу оновлено", "book": book})

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return json_response({"message": "Книгу видалено"})

if __name__ == "__main__":
    app.run(debug=True)