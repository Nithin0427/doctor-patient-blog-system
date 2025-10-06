import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, BlogPost
from config import Config
from utils import save_image
from functools import wraps

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def doctor_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != 'doctor':
                flash('Doctor access required.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated

    def get_categories():
        return ['Mental Health', 'Heart Disease', 'Covid19', 'Immunization']

    @app.route('/')
    def index():
        return render_template('index.html')

    # ---- Auth (simple register/login) ----
    @app.route('/register', methods=['GET','POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username').strip()
            password = request.form.get('password')
            role = request.form.get('role','patient')
            if not username or not password:
                flash('Fill all fields', 'warning')
                return render_template('register.html')
            if User.query.filter_by(username=username).first():
                flash('Username exists', 'warning')
                return render_template('register.html')
            u = User(username=username, password_hash=generate_password_hash(password), role=role)
            db.session.add(u)
            db.session.commit()
            flash('Registered. Please login.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username').strip()
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if not user or not check_password_hash(user.password_hash, password):
                flash('Invalid credentials', 'danger')
                return render_template('login.html')
            login_user(user)
            flash('Logged in', 'success')
            return redirect(url_for('index'))
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Logged out', 'info')
        return redirect(url_for('index'))

    # ---- Doctor routes ----
    @app.route('/doctor/posts/new', methods=['GET','POST'])
    @login_required
    @doctor_required
    def doctor_create_post():
        if request.method == 'POST':
            title = request.form.get('title','').strip()
            category = request.form.get('category')
            summary = request.form.get('summary','').strip()
            content = request.form.get('content','').strip()
            is_draft = request.form.get('is_draft') == 'on'
            image = request.files.get('image')
            if not title or not category or not summary or not content:
                flash('Please fill required fields', 'warning')
                return render_template('doctor_create_post.html', categories=get_categories())
            image_filename = save_image(image) if image else None
            post = BlogPost(
                title=title, image_filename=image_filename, category=category,
                summary=summary, content=content, is_draft=is_draft, author_id=current_user.id
            )
            db.session.add(post)
            db.session.commit()
            flash('Post saved', 'success')
            return redirect(url_for('doctor_my_posts'))
        return render_template('doctor_create_post.html', categories=get_categories())

    @app.route('/doctor/posts')
    @login_required
    @doctor_required
    def doctor_my_posts():
        posts = BlogPost.query.filter_by(author_id=current_user.id).order_by(BlogPost.created_at.desc()).all()
        return render_template('doctor_my_posts.html', posts=posts)

    # ---- Patient/public routes ----
    @app.route('/blogs')
    def blogs_index():
        categories = get_categories()
        cat_counts = {c: BlogPost.query.filter_by(category=c, is_draft=False).count() for c in categories}
        return render_template('blogs_index.html', categories=categories, cat_counts=cat_counts)

    @app.route('/blogs/category/<category_name>')
    def blogs_by_category(category_name):
        categories = get_categories()
        if category_name not in categories:
            flash('Unknown category', 'warning')
            return redirect(url_for('blogs_index'))
        posts = BlogPost.query.filter_by(category=category_name, is_draft=False).order_by(BlogPost.created_at.desc()).all()
        return render_template('blogs_by_category.html', category=category_name, posts=posts)

    @app.route('/blogs/<int:post_id>')
    def blog_detail(post_id):
        post = BlogPost.query.get_or_404(post_id)
        if post.is_draft and (not current_user.is_authenticated or current_user.id != post.author_id):
            flash('Post not available', 'warning')
            return redirect(url_for('blogs_index'))
        return render_template('blog_detail.html', post=post)

    @app.route('/uploads/blog_images/<filename>')
    def uploaded_image(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app

# Expose app for flask run
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
