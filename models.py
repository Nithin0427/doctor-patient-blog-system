from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('doctor','patient', name='user_roles'), nullable=False, default='patient')
    posts = db.relationship('BlogPost', backref='author', lazy=True)

class BlogPost(db.Model):
    __tablename__ = 'blog_post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)
    category = db.Column(db.Enum('Mental Health','Heart Disease','Covid19','Immunization', name='blog_categories'), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_draft = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def summary_truncated(self, max_words=15):
        words = self.summary.split()
        if len(words) <= max_words:
            return self.summary
        return ' '.join(words[:max_words]) + '...'
