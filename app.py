from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kutuphane.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'gizli_key'

db = SQLAlchemy(app)

# -----------------------------
# MODELLER
# -----------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), default="Mevcut")  # Mevcut veya Ödünç Verildi

# -----------------------------
# VERİTABANI OLUŞTURMA
# -----------------------------
with app.app_context():
    db.create_all()

# -----------------------------
# ROUTELAR
# -----------------------------
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            flash("Giriş başarılı!", "success")
            return redirect(url_for('kitaplar'))
        else:
            flash("Kullanıcı adı veya şifre yanlış!", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Kayıt başarılı!", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/kitaplar')
def kitaplar():
    if not session.get('username'):
        flash("Lütfen önce giriş yapın.", "warning")
        return redirect(url_for('login'))
    books = Book.query.all()
    return render_template('kitaplar.html', books=books, username=session['username'])

@app.route('/add_book', methods=['POST'])
def add_book():
    if not session.get('username'):
        flash("Lütfen önce giriş yapın.", "warning")
        return redirect(url_for('login'))
    title = request.form['title']
    author = request.form['author']
    if title and author:
        new_book = Book(title=title, author=author)
        db.session.add(new_book)
        db.session.commit()
        flash(f"{title} eklendi!", "success")
    else:
        flash("Lütfen başlık ve yazar girin.", "danger")
    return redirect(url_for('kitaplar'))

@app.route('/update_status/<int:book_id>')
def update_status(book_id):
    if not session.get('username'):
        flash("Lütfen önce giriş yapın.", "warning")
        return redirect(url_for('login'))
    book = Book.query.get(book_id)
    if book:
        book.status = "Ödünç Verildi" if book.status == "Mevcut" else "Mevcut"
        db.session.commit()
        flash(f"{book.title} durumu güncellendi.", "success")
    else:
        flash("Kitap bulunamadı!", "danger")
    return redirect(url_for('kitaplar'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Çıkış yapıldı.", "info")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
