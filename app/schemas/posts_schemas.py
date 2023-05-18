from ..extensions import db, ma

# Post model, and schemas
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(50))
    body = db.Column(db.String(255))

    def __repr__(self):
        return '<Post %s>' % self.title

class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "title", "body")

post_schema = PostSchema()
posts_schema = PostSchema(many=True)