from flask import Flask, render_template, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
import os

app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
connection = psycopg2.connect(
    dbname=os.environ.get('DB_NAME', 'projectdb'),
    user=os.environ.get('DB_USER', 'postgres'),
    password=os.environ.get('DB_PASSWORD', ''),
    host=os.environ.get('DB_HOST', 'localhost'),
    port=os.environ.get('DB_PORT', '5432')
)

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

cursor = connection.cursor()
app = Flask(__name__)
def auth(username, password):
    print("результат")
    # Используем параметризованный запрос для предотвращения SQL-инъекций
    cursor.execute("SELECT username, password FROM Users WHERE username = %s;", (username,))
    row = cursor.fetchone()
    if row:
        if check_password_hash(row[1], password):  # Проверяем хэш пароля
            session['username'] = username  # Сохраняем имя пользователя в сессии
            user = User(username, "user")
            return "authorization completed"
        else:
            return "authorization failed: incorrect password"
    else:
        return "the user does not exist"
def insert_to_db():
    text = "Lorem ipsum"
    # Проверяем, есть ли уже такой пост в базе данных, чтобы избежать дубликатов
    cursor.execute("SELECT id FROM Posts WHERE name = %s AND author = %s;", ("Пост1", "admin"))
    existing_post = cursor.fetchone()
    if not existing_post:
        cursor.execute("INSERT INTO Posts(name, text, author) VALUES(%s, %s, %s);", ("Пост1", text, "admin"))
    cursor.execute("SELECT * FROM Posts;")
    rows = cursor.fetchall()
    return rows
@app.route('/home')
def home():
    return render_template('index.html')
@app.route('/chat')
def chat():
    return render_template('chat.html')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/calendar')
def calendar():
    return render_template('calendar.html')
@app.route('/articles')
def articles():
    # Получаем все посты из базы данных
    cursor.execute("SELECT name, text, author FROM Posts;")
    posts = cursor.fetchall()
    # Передаем посты в шаблон
    return render_template('articles.html', posts=posts)

@app.route('/login', methods = ['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    # Хэшируем пароль перед проверкой (предполагая, что в базе хранятся хэшированные пароли)
    result = auth(username, password)
    if result == "authorization completed":
        return render_template("index.html")
    else:
        return "Нету пользователя"
def login():
    return render_template('login.html')
# http://127.0.0.1:5000/home

if __name__ == '__main__':  
    # Запускаем функцию для добавления начальных данных при старте приложения
    posts = insert_to_db()  # Получаем посты после вставки
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    
# CREATE TABLE Users(id SERIAL PRIMARY KEY, username VARCHAR(30), password VARCHAR(20), name VARCHAR(40)); таблица пользователей
    
# CREATE TABLE Posts(id SERIAL PRIMARY KEY, name VARCHAR(30), text VARCHAR(2000), author VARCHAR(30));- таблица постов
