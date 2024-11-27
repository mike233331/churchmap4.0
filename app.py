from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # Укажите вашу строку подключения к базе данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключает предупреждения SQLAlchemy
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
db = SQLAlchemy(app)
CORS(app)  # Разрешаем CORS для всех маршрутов

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    built = db.Column(db.String(4), nullable=False)
    coordinates = db.Column(db.String(50), nullable=False)
    architect = db.Column(db.String(50), nullable=False)
    relig = db.Column(db.String(50), nullable=False)
    photos = db.Column(db.Text)  # Поле для хранения путей к фото (разделённых запятыми)


with app.app_context():
    db.create_all()


# Новый маршрут для получения задачи по id
@app.route('/todo/<int:id>', methods=['GET'])
def get_todo_by_id(id):
    todo = Todo.query.get(id)
    if todo:
        return jsonify({
            'id': todo.id,
            'text': todo.text,
            'country': todo.country,
            'city': todo.city,
            'built': todo.built,
            'coordinates': todo.coordinates,
            'architect': todo.architect,
            'relig': todo.relig
        })
    return jsonify({'message': 'Task not found'}), 404


# Маршрут для получения всех задач
@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([
        {
            'id': todo.id,
            'text': todo.text,
            'country': todo.country,
            'city': todo.city,
            'built': todo.built,
            'coordinates': todo.coordinates,
            'architect': todo.architect,
            'relig': todo.relig
        } for todo in todos
    ])

# Маршрут для добавления новой задачи
@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.form
    files = request.files.getlist('photos')
    photo_paths = []

    # Обработка файлов
    if files:
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                photo_paths.append(filepath)

    # Добавление задачи в базу данных
    new_todo = Todo(
        text=data.get('text'),
        country=data.get('country'),
        city=data.get('city'),
        built=data.get('built'),
        coordinates=data.get('coordinates'),
        architect=data.get('architect'),
        relig=data.get('relig'),
        photos=','.join(photo_paths)  # Сохраняем пути к фото
    )
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message': 'Задача добавлена', 'id': new_todo.id}), 201

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Создаем папку, если её нет
    app.run(debug=True)

# Маршрут для обновления задачи
@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    todo = Todo.query.get(id)
    if todo:
        todo.text = data.get('text', todo.text)
        todo.country = data.get('country', todo.country)
        todo.city = data.get('city', todo.city)
        todo.built = data.get('built', todo.built)
        todo.coordinates = data.get('coordinates', todo.coordinates)
        todo.architect = data.get('architect', todo.architect)
        todo.relig = data.get('relig', todo.relig)
        db.session.commit()
        return jsonify({'message': 'Task updated successfully'})
    return jsonify({'message': 'Task not found'}), 404

# Маршрут для удаления задачи
@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})
    return jsonify({'message': 'Task not found'}), 404


# Главная страница будет отдавать index.html
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
