from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    send_hour = db.Column(db.Integer, default=12)
    categories = db.Column(db.String(255), nullable=False)
    time_zone = db.Column(db.String(64), default='UTC')

    def __repr__(self):
        return f"<Subscriber {self.email}>"
