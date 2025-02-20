from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

# Create Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main_users.db'  # Main database
app.config['SECRET_KEY'] = 'your-secret-key'  # For session management
db = SQLAlchemy(app)

# User model for main database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    db_name = db.Column(db.String(120), unique=True, nullable=False)

# Function to create a new database for each user and insert initial data
# Function to create a new database for each user and insert initial data
def create_user_database(username):
    db_name = f"user_{username}.db"
    
    user_app = Flask(f"user_app_{username}")
    user_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    user_db = SQLAlchemy(user_app)
    
    class Note(user_db.Model):
        id = user_db.Column(user_db.Integer, primary_key=True)
        note = user_db.Column(user_db.String(200), default="this data from user's database")    
    
    with user_app.app_context():
        user_db.create_all()
        
        # التأكد من عدم وجود بيانات قبل الإضافة
        if not Note.query.first():
            initial_note = Note(note="Welcome to your personal database!")
            user_db.session.add(initial_note)
            user_db.session.commit()
    
    return db_name


# Function to remove users whose database files are missing
def remove_users_with_missing_databases():
    users = User.query.all()
    for user in users:
        if not os.path.exists(user.db_name):
            db.session.delete(user)
    db.session.commit()

# Function to get user notes from their database
def get_user_note(username):
    user_app = Flask(f"user_app_{username}")
    user_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///user_{username}.db'
    user_db = SQLAlchemy(user_app)
    
    class Note(user_db.Model):
        id = user_db.Column(user_db.Integer, primary_key=True)
        note = user_db.Column(user_db.String(200))
    
    with user_app.app_context():
        note = Note.query.first()
        return note.note if note else "No note found"

# Login/Register page
@app.route('/', methods=['GET', 'POST'])
def login():
    remove_users_with_missing_databases()  # Remove users with missing databases
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user:
            if user.password == password:
                session['username'] = username
                session['db_name'] = user.db_name
                return redirect(url_for('dashboard'))
            return "Wrong password!"
        else:
            try:
                db_name = create_user_database(username)
                new_user = User(username=username, password=password, db_name=db_name)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                session['db_name'] = db_name
                return redirect(url_for('dashboard'))
            except Exception as e:
                return f"Error creating account: {str(e)}"
    
    return render_template_string("""
        <h1>Login or Register</h1>
        <form method="POST">
            Username: <input type="text" name="username" required><br>
            Password: <input type="password" name="password" required><br>
            <input type="submit" value="Login/Register">
        </form>
    """)

# Dashboard page
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_note = get_user_note(session['username'])
    
    return render_template_string("""
        <h1>Welcome {{ username }}!</h1>
        <p>You are connected to your personal database: {{ db_name }}</p>
        <p>{{ note }}</p>
        <a href="{{ url_for('logout') }}">Logout</a>
    """, username=session['username'], db_name=session['db_name'], note=user_note)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
