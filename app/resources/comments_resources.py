from flask import request
from flask_restx import Resource, Namespace
from ..extensions import basic_auth, db
from ..schemas.comments_schemas import Comment, comments_schema, comment_schema

comments_ns = Namespace("api/comments")

@comments_ns.route("")
class Comments(Resource):
    @basic_auth.required
    def get(self):
        comments = Comment.query.all()
        return comments_schema.dump(comments)

    @basic_auth.required
    def post(self):
        new_comment = Comment(
            name=request.json['name'],
            body=request.json['body'],
            post_id=request.json['post_id'],
            email=request.json['email']
        )
        db.session.add(new_comment)
        db.session.commit()
        return comment_schema.dump(new_comment)

@comments_ns.route("/<int:comment_id>")
class Comments(Resource):
    # Not required but added to complete CRUD functionality
    @basic_auth.required
    def get(self, comment_id):
        comment = db.session.get(Comment, comment_id)
        return comment_schema.dump(comment)

    # Not required but added to complete CRUD functionality
    @basic_auth.required
    def patch(self, comment_id):
        comment = db.session.get(Comment, comment_id)

        if 'name' in request.json:
            comment.name = request.json['name']
        if 'body' in request.json:
            comment.body = request.json['body']
        if 'post_id' in request.json:
            comment.post_id = request.json['post_id']
        if 'email' in request.json:
            comment.email = request.json['email']

        db.session.commit()
        return comment_schema.dump(comment)

    @basic_auth.required
    def delete(self, comment_id):
        comment = db.session.get(Comment, comment_id)
        db.session.delete(comment)
        db.session.commit()
        return '', 204
