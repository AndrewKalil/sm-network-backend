from ..extensions import db, ma

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    body = db.Column(db.String(255))

    def __repr__(self):
        return '<Post %s>' % self.name

class CommentSchema(ma.Schema):
    class Meta:
        fields = ("id", "post_id", "name", "email", "body")

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)