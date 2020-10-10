from flask import jsonify, Blueprint, abort

from flask_restful import (Resource, Api, reqparse,
                               fields, marshal, marshal_with)

from auth import auth
import models

book_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.String
}

def book_or_404(book_id):
    try:
        book = models.Book.get(models.Book.id==book_id)
    except models.Book.DoesNotExist:
        abort(404)
    else:
        return book


class BookList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=True,
            help='No book title provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'author',
            required=True,
            help='No author provided',
            location=['form', 'json']
        )
        super().__init__()
        
    def get(self):
        books = [marshal(book, book_fields)
                   for book in models.Book.select()]
        return {'books': books}
    
    @marshal_with(book_fields)
    @auth.login_required
    def post(self):
        args = self.reqparse.parse_args()
        book = models.Book.create(**args)
        return book, 201


class Book(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=True,
            help='No book title provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'author',
            required=True,
            help='No book URL provided',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(book_fields)
    def get(self, id):
        return book_or_404(id)
    
    @marshal_with(book_fields)
    @auth.login_required
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Book.update(**args).where(models.Book.id==id)
        query.execute()
        return models.Book.get(models.Book.id==id), 200

    @auth.login_required
    def delete(self, id):
        query = models.Book.delete().where(models.Book.id==id)
        query.execute()
        return 'Book deleted', 200

books_api = Blueprint('resources.books', __name__)
api = Api(books_api)
api.add_resource(
    BookList,
    '/books',
    endpoint='books'
)
api.add_resource(
    Book,
    '/books/<int:id>',
    endpoint='book'
)