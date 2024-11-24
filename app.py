from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# db = SQLAlchemy(app)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # Укажите вашу строку подключения к базе данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключает предупреждения SQLAlchemy
db = SQLAlchemy(app)
CORS(app)  # Разрешаем CORS для всех маршрутов




class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    built = db.Column(db.String(20), nullable=False)
    coordinates = db.Column(db.String(40), nullable=False)
    architect = db.Column(db.String(60), nullable=False)
    relig = db.Column(db.String(100), nullable=False)

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
    data = request.get_json()
    new_todo = Todo(
        text=data['text'],
        country=data['country'],
        city=data['city'],
        built=data['built'],
        coordinates=data['coordinates'],
        architect=data['architect'],
        relig=data['relig']
    )
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({
        'id': new_todo.id,
        'text': new_todo.text,
        'country': new_todo.country,
        'city': new_todo.city,
        'built': new_todo.built,
        'coordinates': new_todo.coordinates,
        'architect': new_todo.architect,
        'relig': new_todo.relig
    })



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

if __name__ == '__main__':
    app.run(debug=True)
