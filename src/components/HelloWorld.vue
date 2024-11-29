<template>
  <div class="todo-app">
    <!-- Кнопка для перехода на страницу добавления задачи -->
    <button @click="goToAddTodoPage" class="add-todo-button">Добавить задачу</button>

    <ul class="todo-list">
      <li v-for="todo in todos" :key="todo.id" class="todo-item">
        <div v-if="editingTodo !== todo" class="todo-text" @click="viewTodo(todo.id)">
          <span>{{ todo.text }}</span>
        </div>
        <div v-else class="edit-fields">
          <input v-model="editedText" :placeholder="todo.text" class="todo-input-edit">
          <input v-model="editedCountry" :placeholder="todo.country" class="todo-input-edit">
          <input v-model="editedCity" :placeholder="todo.city" class="todo-input-edit">
          <input v-model="editedBuilt" :placeholder="todo.built" class="todo-input-edit">
          <input v-model="editedCoordinates" :placeholder="todo.coordinates" class="todo-input-edit">
          <input v-model="editedArchitect" :placeholder="todo.architect" class="todo-input-edit">
          <input v-model="editedReligion" :placeholder="todo.relig" class="todo-input-edit">
        </div>
        <div class="button-group">
          <button @click="removeTodo(todo.id)" class="delete-button">Удалить</button>
          <button v-if="editingTodo !== todo" @click="startEditing(todo)" class="edit-button">Редактировать</button>
          <button v-if="editingTodo === todo" @click="saveEdit" class="save-button">Сохранить</button>
          <button v-if="editingTodo === todo" @click="cancelEdit" class="cancel-button">Отменить</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const todos = ref([])
const editingTodo = ref(null)
const editedText = ref('')
const editedCountry = ref('')
const editedCity = ref('')
const editedBuilt = ref('')
const editedCoordinates = ref('')
const editedArchitect = ref('')
const editedReligion = ref('')
const router = useRouter()

async function fetchTodos() {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/todos')
    todos.value = response.data
  } catch (error) {
    console.error('Ошибка при получении задач:', error)
  }
}

async function removeTodo(todoId) {
  try {
    await axios.delete(`http://127.0.0.1:5000/api/todos/${todoId}`)
    todos.value = todos.value.filter(todo => todo.id !== todoId)
  } catch (error) {
    console.error('Ошибка при удалении задачи:', error)
  }
}

function startEditing(todo) {
  editingTodo.value = todo
  editedText.value = todo.text
  editedCountry.value = todo.country
  editedCity.value = todo.city
  editedBuilt.value = todo.built
  editedCoordinates.value = todo.coordinates
  editedArchitect.value = todo.architect
  editedReligion.value = todo.relig
}

async function saveEdit() {
  if (editedText.value.trim()) {
    try {
      const response = await axios.put(`http://127.0.0.1:5000/api/todos/${editingTodo.value.id}`, {
        text: editedText.value,
        country: editedCountry.value,
        city: editedCity.value,
        built: editedBuilt.value,
        coordinates: editedCoordinates.value,
        architect: editedArchitect.value,
        relig: editedReligion.value
      })
      if (response.data.message === 'Task updated successfully') {
        Object.assign(editingTodo.value, {
          text: editedText.value,
          country: editedCountry.value,
          city: editedCity.value,
          built: editedBuilt.value,
          coordinates: editedCoordinates.value,
          architect: editedArchitect.value,
          relig: editedReligion.value
        })
        editingTodo.value = null
        editedText.value = editedCountry.value = editedCity.value = editedBuilt.value = editedCoordinates.value = editedArchitect.value = editedReligion.value = ''
      }
    } catch (error) {
      console.error('Ошибка при сохранении задачи:', error)
    }
  }
}

function cancelEdit() {
  editingTodo.value = null
  editedText.value = editedCountry.value = editedCity.value = editedBuilt.value = editedCoordinates.value = editedArchitect.value = editedReligion.value = ''
}

function viewTodo(todoId) {
  router.push(`/todo/${todoId}`)
}

// Переход на страницу добавления задачи
function goToAddTodoPage() {
  router.push('/addchurch')
}

// Загрузка задач
fetchTodos()
</script>

<style scoped>
/* Кнопка для добавления задачи */
.add-todo-button {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin-bottom: 20px;
}

.add-todo-button:hover {
  background-color: #388e3c;
}

.todo-list {
  background-color: white;
  opacity: 0.85; /* 80% непрозрачности */
  border-radius: 10px;
  list-style-type: none;
  padding: 0;
  margin: 20px auto;
  max-width: 600px;
}

.todo-item {
  background-color: #ffffff;
  padding: 15px;
  margin: 10px 0;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.todo-text {
  font-size: 18px;
  color: #00796b;
  flex-grow: 1;
}

.todo-input-edit {
  width: 100%;
  padding: 8px;
  margin: 5px 0;
  border: 1px solid #b2dfdb;
  border-radius: 5px;
  background-color: #f0f8ff;
  font-size: 14px;
}

.edit-button,
.save-button,
.cancel-button,
.delete-button {
  padding: 8px 16px;
  border-radius: 5px;
  font-size: 14px;
  border: none;
  cursor: pointer;
}

.edit-button {
  background-color: #0097a7;
  color: white;
}

.edit-button:hover {
  background-color: #146670;
}

.save-button {
  background-color: #4caf50;
  color: white;
}

.save-button:hover {
  background-color: #388e3c;
}

.cancel-button {
  background-color: #fbc02d;
  color: white;
}

.cancel-button:hover {
  background-color: #f9a825;
}

.delete-button {
  background-color: #d32f2f;
  color: white;
}

.delete-button:hover {
  background-color: #ff0000;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-content: flex-end;
  width: 100%;
  align-items: flex-end;
}
</style>