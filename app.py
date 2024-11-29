from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # Подключение к базе данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключение предупреждений SQLAlchemy
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
db = SQLAlchemy(app)
CORS(app)  # Разрешение CORS для всех маршрутов

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

# Функция для проверки допустимых типов файлов
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Маршрут для получения списка всех задач
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

# Маршрут для получения задачи по ID
@app.route('/todo/<int:id>', methods=['GET'])
def get_todo_by_id(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({'message': 'Task not found'}), 404

    photos = [
        {'filename': os.path.basename(photo), 'filepath': f'/uploads/{os.path.basename(photo)}'}
        for photo in todo.photos.split(',') if photo
    ]

    return jsonify({
        'id': todo.id,
        'text': todo.text,
        'country': todo.country,
        'city': todo.city,
        'built': todo.built,
        'coordinates': todo.coordinates,
        'architect': todo.architect,
        'relig': todo.relig,
        'photos': photos
    })

# Маршрут для добавления новой задачи
@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.form
    files = request.files.getlist('photos')
    photo_paths = []

    if files:
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                photo_paths.append(filepath)

    new_todo = Todo(
        text=data.get('text'),
        country=data.get('country'),
        city=data.get('city'),
        built=data.get('built'),
        coordinates=data.get('coordinates'),
        architect=data.get('architect'),
        relig=data.get('relig'),
        photos=','.join(photo_paths)
    )
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message': 'Task added successfully', 'id': new_todo.id}), 201


@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({'message': 'Task not found'}), 404

    todo.text = data.get('text', todo.text)
    todo.country = data.get('country', todo.country)
    todo.city = data.get('city', todo.city)
    todo.built = data.get('built', todo.built)
    todo.coordinates = data.get('coordinates', todo.coordinates)
    todo.architect = data.get('architect', todo.architect)
    todo.relig = data.get('relig', todo.relig)

    # Обновляем фотографии, если они переданы
    if 'photos' in data:
        todo.photos = ",".join(data['photos'])  # Сохраняем список фотографий как строку через запятую

    db.session.commit()

    return jsonify({'message': 'Task updated successfully'})


# Маршрут для удаления задачи
@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({'message': 'Task not found'}), 404

    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

# Маршрут для загрузки файлов
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Главная страница
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Создаём папку, если её нет
    app.run(debug=True)