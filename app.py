import json

from flask import Flask, jsonify, request, Response
from werkzeug.exceptions import abort

# TODO: integration tests using .json
# TODO: prevent dupe POST
# TODO: add validations on PUT
# TODO: add PATCH
# TODO: add DELETE
# TODO: .json to own folder

"""
NOTES

* definition of a framework: receive req, route to controller, dispatch from controller, return res
* `jsonify()` dict ➡️ json, add HTTP headers
* `request.json` returns dict
* docs 1.3.2 say use `SimpleJSON`, why is course using `jsonify`?
* when did they get rid of the `app.run(port=5000)` bit?
* JWT -> https://github.com/vimalloc/flask-jwt-extended

"""

app = Flask(__name__)

# IN-MEM DATA STORE


books = [
    {
        'name': 'Origins of Political Order',
        'price': 10.00,
        'isbn': '0374533229',
    },
    {
        'name': 'Political Order and Political Decay',
        'price': 10.00,
        'isbn': '0374535620',
    }
]

# UTIL


def handle_invalid_post_key_missing(book):
    if 'name' in book and 'price' in book and 'isbn' in book:  # idky but Flask complains if not on one-line
        return True
    else:
        return False


def handle_invalid_post_key_wrong(book):
    """point here is to exclude any extraneous keys"""
    return {
        'name': book['name'],
        'price': book['price'],
        'isbn': book['isbn'],
    }


def lookup_by_isbn(lookup):
    for book in books:
        if book['isbn'] == lookup:
            return book

# ROUTES


@app.route('/books')
def get_books():
    return jsonify({'books': books})


@app.route('/books/count')
def get_books_count():
    return jsonify({'book_count': len(books)})


@app.route('/books/<string:isbn>')
def get_book(isbn):
    for book in books:
        if book['isbn'] == isbn:
            return jsonify({'book': book})
        # TODO: remove else block and put return outside loop
        else:
            err_msg = {'error': 'invalid book object'}
            # TODO: rf to use this in 200
            # TODO: mimetype necessary each time? if so, store in const
            res = Response(json.dumps(err_msg), 404, mimetype='application/json')
            return res


@app.route('/books', methods=['POST'])
def post_book():
    new_book = request.get_json()
    if handle_invalid_post_key_missing(new_book):
        validated_book = handle_invalid_post_key_wrong(new_book)
        books.insert(0, validated_book)
        res = Response('', 201, mimetype='application/json')  # TODO: tlrd for mimetype
        # TODO: why does this mangle the ISBN
        # res.headers['Location'] = '{} {}'.format('/books/', validated_book['isbn'])
        # TODO: research HTTP 'Location' header
        res.headers['Location'] = '/books/' + str(validated_book['isbn'])
        return res  # TODO return json of created

    else:
        # TODO: mv to else of handle_invalid_post_key_missing
        return abort(400)


@app.route('/books/<string:isbn>', methods=['PUT'])
def put_book(isbn):
    # TODO client sending isbn in URL so payload should only be name and price
    new_book = request.get_json()
    book_to_update = lookup_by_isbn(isbn)
    # TODO validate, add 204 status code
    if book_to_update:
        books[books.index(book_to_update)] = new_book
        return jsonify({'book': new_book})
    else:
        abort(404)
