<template>
  <div class="todo-app">
    <!-- Кнопка для перехода на страницу добавления задачи -->
    <button @click="goToAddTodoPage" class="add-todo-button">Добавить задачу</button>

    <ul class="todo-list">
      <li v-for="todo in todos" :key="todo.id" class="todo-item">
        <div class="todo-text" @click="viewTodo(todo.id)">
          <span>{{ todo.text }}</span>
        </div>
        <div class="button-group">
          <button @click="removeTodo(todo.id)" class="delete-button">Удалить</button>
          <button @click="goToEditPage(todo.id)" class="edit-button">Редактировать</button>
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
const router = useRouter()

// Загружаем задачи
async function fetchTodos() {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/todos')
    todos.value = response.data
  } catch (error) {
    console.error('Ошибка при получении задач:', error)
  }
}

// Удаление задачи
async function removeTodo(todoId) {
  try {
    await axios.delete(`http://127.0.0.1:5000/api/todos/${todoId}`)
    todos.value = todos.value.filter(todo => todo.id !== todoId)
  } catch (error) {
    console.error('Ошибка при удалении задачи:', error)
  }
}

// Переход на страницу редактирования задачи
function goToEditPage(todoId) {
  router.push(`/changes/${todoId}`)
}

// Переход на страницу добавления задачи
function goToAddTodoPage() {
  router.push('/addchurch')
}

// Переход на страницу просмотра задачи
function viewTodo(todoId) {
  router.push(`/todo/${todoId}`)
}

// Загрузка задач при монтировании компонента
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

.edit-button,
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
