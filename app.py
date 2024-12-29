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

# Модель для таблицы религий
class Religion(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор религии
    name = db.Column(db.String(100), nullable=False)  # Название религии
    description = db.Column(db.Text)  # Описание религии (необязательно)

    def __repr__(self):
        return f'<Religion {self.name}>'

# Модель для таблицы задач (Todo)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    built = db.Column(db.String(4), nullable=False)
    coordinates = db.Column(db.String(50), nullable=False)
    architect = db.Column(db.String(50), nullable=False)
    religion_id = db.Column(db.Integer, db.ForeignKey('religion.id'), nullable=False)  # Внешний ключ
    photos = db.Column(db.Text)  # Поле для хранения путей к фото (разделённых запятыми)

    religion = db.relationship('Religion', backref=db.backref('todos', lazy=True))  # Связь с таблицей Religion

with app.app_context():
    db.create_all()

    # Добавление нескольких религий, если таблица пуста
    if Religion.query.count() == 0:
        religion1 = Religion(name='Христианство', description='Религия, основанная на жизни и учении Иисуса Христа.')
        religion2 = Religion(name='Ислам', description='Религия, основанная на учении пророка Мухаммеда.')
        db.session.add(religion1)
        db.session.add(religion2)
        db.session.commit()

# Функция для проверки допустимых типов файлов
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Маршрут для получения списка всех религий
@app.route('/api/religions', methods=['GET'])
def get_religions():
    religions = Religion.query.all()
    return jsonify([
        {
            'id': religion.id,
            'name': religion.name,
            'description': religion.description
        } for religion in religions
    ])

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
            'religion': todo.religion_id  # Ссылаемся на имя религии
        } for todo in todos
    ])


@app.route('/todo/<int:id>', methods=['GET'])
def get_todo_by_id(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({'message': 'Task not found'}), 404

    # Получаем религию, если она существует
    religion_name = todo.religion.name if todo.religion else None

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
        'religion_name': religion_name,  # Ссылаемся на имя религии
        'photos': photos
    })


# Маршрут для добавления новой задачи
@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.form
    files = request.files.getlist('photos')
    photo_filenames = []  # Сохраняем только имена файлов

    if files:
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                photo_filenames.append(filename)  # Сохраняем имя файла

    # Получаем ID религии из формы
    religion_id = data.get('religion_id')

    new_todo = Todo(
        text=data.get('text'),
        country=data.get('country'),
        city=data.get('city'),
        built=data.get('built'),
        coordinates=data.get('coordinates'),
        architect=data.get('architect'),
        religion_id=religion_id,  # Сохраняем ID религии
        photos=','.join(photo_filenames)  # Сохраняем имена файлов через запятую
    )
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message': 'Task added successfully', 'id': new_todo.id}), 201


# Маршрут для обновления задачи
@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({'message': 'Task not found'}), 404

    # Проверяем, был ли запрос в формате JSON или обычной формы
    if request.is_json:
        data = request.get_json()  # Для JSON
    else:
        data = request.form  # Для формы

    # Обновляем поля
    todo.text = data.get('text', todo.text)
    todo.country = data.get('country', todo.country)
    todo.city = data.get('city', todo.city)
    todo.built = data.get('built', todo.built)
    todo.coordinates = data.get('coordinates', todo.coordinates)
    todo.architect = data.get('architect', todo.architect)
    todo.religion_id = data.get('religion_id', todo.religion_id)  # Обновляем религию

    # Обрабатываем фотографии, если они есть
    photo_filenames = []  # Список для новых фотографий
    files = request.files.getlist('photos')
    if files:
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                photo_filenames.append(filename)  # Добавляем имя файла в список

    # Если есть новые фотографии, обновляем их
    if photo_filenames:
        todo.photos = ",".join(photo_filenames)  # Обновляем поле с фотографиями

    # Сохраняем изменения в базе данных
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

# Маршрут для удаления фотографии
@app.route('/api/todos/<int:id>/photos/<filename>', methods=['DELETE'])
def delete_photo(id, filename):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({'message': 'Task not found'}), 404

    # Получаем все имена файлов
    photos = todo.photos.split(',')
    print(f"Фотографии в базе данных для задачи {id}: {photos}")  # Логируем все фотографии

    if filename in photos:
        print(f"Удаляем фото: {filename}")  # Логируем имя файла

        # Удаляем фото из списка
        photos.remove(filename)
        todo.photos = ",".join(photos)  # Обновляем список фотографий в базе данных

        # Путь к файлу на сервере
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Путь к файлу для удаления: {photo_path}")  # Логируем путь к файлу на сервере

        # Проверяем, существует ли файл
        if os.path.exists(photo_path):
            os.remove(photo_path)
            print(f"Фото {filename} успешно удалено с диска.")  # Логируем успешное удаление
        else:
            print(f"Фото {filename} не найдено на диске.")  # Логируем ошибку

        db.session.commit()  # Сохраняем изменения в базе данных
        return jsonify({'message': 'Photo deleted successfully'}), 200
    else:
        return jsonify({'message': 'Photo not found in task'}), 404

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
