from flask import request
from flask_restx import Resource, Namespace
from ..extensions import basic_auth, db
from ..schemas.posts_schemas import Post, posts_schema, post_schema
from ..schemas.comments_schemas import Comment, comments_schema

posts_ns = Namespace("api/posts")

@posts_ns.route("")
class Posts(Resource):
    @basic_auth.required
    def get(self):
        posts = Post.query.all()
        return posts_schema.dump(posts)

    @basic_auth.required
    def post(self):
        new_post = Post(
            title=request.json['title'],
            body=request.json['body'],
            user_id=request.json['user_id'],
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)

@posts_ns.route("/<int:post_id>")
class Posts(Resource):
    # Not required but added to complete CRUD functionality
    @basic_auth.required
    def get(self, post_id):
        post = db.session.get(Post, post_id)
        return post_schema.dump(post)

    # Not required but added to complete CRUD functionality
    @basic_auth.required
    def patch(self, post_id):
        post = db.session.get(Post, post_id)

        if 'title' in request.json:
            post.title = request.json['title']
        if 'body' in request.json:
            post.body = request.json['body']
        if 'user_id' in request.json:
            post.user_id = request.json['user_id']

        db.session.commit()
        return post_schema.dump(post)

    @basic_auth.required
    def delete(self, post_id):
        post = db.session.get(Post, post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204

@posts_ns.route("/<int:post_id>/comments")
class Posts(Resource):
    @basic_auth.required
    def get(self, post_id):
        comments = db.session.query(Comment).filter(Comment.post_id == post_id)
        print(comments)
        return comments_schema.dump(comments)