# from app import db

# class Quote(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     quote = db.Column(db.String(500), nullable=False)
#     author = db.Column(db.String(100), nullable=False)
#     category = db.Column(db.String(100), nullable=False)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'quote': self.quote,
#             'author': self.author,
#             'category': self.category
#         }
