# Flask Blog System 

This project adds a simple blog feature to a Flask app where **doctors** can create posts (draft support)
and **patients** can view published posts by category.

## Features
- 4 categories: Mental Health, Heart Disease, Covid19, Immunization
- Doctor: create posts with Title, Image, Category, Summary, Content, Draft flag
- Doctor: view own posts
- Patient: view published posts by category; summaries truncated to 15 words
- MySQL (SQLAlchemy) as database
- Images stored in `static/uploads/blog_images/`
- Bootstrap styling (simple)

## Quick start (development)
1. Create a Python virtual environment and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables (example):
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export DATABASE_URL='mysql+pymysql://user:password@localhost/blogdb'
   export SECRET_KEY='replace-me'
   ```
4. Create the upload folder:
   ```bash
   mkdir -p static/uploads/blog_images
   ```
5. Initialize the database and create a sample doctor & patient:
   ```bash
   python create_db.py
   ```
   `create_db.py` 
   will attempt to create tables and add two users:
   - doctor / doctorpass (role: doctor)
   - patient / patientpass (role: patient)

6. Run the app:
   ```bash
   flask run python app.py
   ```
7. Open `http://127.0.0.1:5000/` and log in with the sample users.

## Notes
- The project uses server-side image storage. For production, consider S3 or other providers.
- Content is stored as plain HTML from a textarea. If you allow rich HTML, sanitize before saving.
