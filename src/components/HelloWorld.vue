<template>
  <div class="todo-app">
    <form @submit.prevent="addTodo" class="todo-form">
      <div class="column-right">
        <input v-model="title" required placeholder="Добавьте название" class="todo-input" :minlength="3" :maxlength="100">
        <input v-model="country" required placeholder="Добавьте страну" class="todo-input" :minlength="3" :maxlength="50">
        <input v-model="architect" required placeholder="Добавьте имя архитектора" class="todo-input" :minlength="3" :maxlength="50">
        <input v-model="city" required placeholder="Добавьте город" class="todo-input" :minlength="3" :maxlength="50">
      </div>

      <div class="column-left">
        <input v-model="built" required placeholder="Добавьте дату строительства" class="todo-input" :minlength="4" :maxlength="4">
        <input v-model="religion" required placeholder="Добавьте религию" class="todo-input" :minlength="3" :maxlength="50">
        <input v-model="coordinates" required placeholder="Добавьте координаты" class="todo-input" :minlength="5" :maxlength="50">
        <button class="todo-button">Добавить</button>
      </div>
    </form>

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

const title = ref('')
const country = ref('')
const architect = ref('')
const city = ref('')
const built = ref('')
const religion = ref('')
const coordinates = ref('')
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

async function addTodo() {
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/todos', {
      text: title.value,
      country: country.value,
      city: city.value,
      built: built.value,
      coordinates: coordinates.value,
      architect: architect.value,
      relig: religion.value
    })
    todos.value.push(response.data)
    title.value = country.value = architect.value = city.value = built.value = religion.value = coordinates.value = ''
  } catch (error) {
    console.error('Ошибка при добавлении задачи:', error)
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

fetchTodos()
</script>

<style scoped>


/* Оформление для формы */
.todo-form {
  background-color: #ffffff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 20px auto;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

/* Стили для полей ввода */
.todo-input {
  width: 100%;
  padding: 8px;
  margin: 5px 0;
  border: 1px solid #b2dfdb;
  border-radius: 5px;
  background-color: #f0f8ff;
  font-size: 14px;
}

/* Стили для кнопки добавить */
.todo-button {
  width: 105%; /* Кнопка будет такой же ширины, как и поля ввода */
  padding: 7.80px; /* Увеличен отступ для высоты */
  background-color: #00bcd4; /* Светло-синий */
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px; /* Увеличен размер текста */
  cursor: pointer;
  margin-top: 5px; /* Увеличен отступ сверху */
}

.todo-button:hover {
  background-color: #0097a7; /* Темный светло-синий при наведении */
}

/* Размещение полей ввода */
.column-left,
.column-right {
  display: flex;
  flex-direction: column;
  flex: 1;
  max-width: 45%;
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

/* Оформление для текста задачи */
.todo-text {
  font-size: 18px;
  color: #00796b;
  flex-grow: 1;
}

/* Оформление для полей редактирования */
.todo-input-edit {
  width: 100%;
  padding: 8px;
  margin: 5px 0;
  border: 1px solid #b2dfdb;
  border-radius: 5px;
  background-color: #f0f8ff;
  font-size: 14px;
}

/* Стили для кнопок редактирования */
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

/* Цвет кнопки "Редактировать" */
.edit-button {
  background-color: #0097a7; /* Темно-синий */
  color: white;
}

.edit-button:hover {
  background-color: #146670; /* Более темный синий при наведении */
}

/* Цвет кнопки "Сохранить" */
.save-button {
  background-color: #4caf50;
  color: white;
}

.save-button:hover {
  background-color: #388e3c;
}

/* Цвет кнопки "Отменить" */
.cancel-button {
  background-color: #fbc02d;
  color: white;
}

.cancel-button:hover {
  background-color: #f9a825;
}

/* Цвет кнопки "Удалить" */
.delete-button {
  background-color: #d32f2f; /* Темно-красный */
  color: white;
}

.delete-button:hover {
  background-color: #ff0000; /* Более темный красный при наведении */
}

/* Размещение кнопок в столбик */
.button-group {
  display: flex;
  flex-direction: column; /* Размещение кнопок в столбик */
  gap: 10px; /* Отступы между кнопками */
  justify-content: flex-end;
  width: 100%; /* Ширина 100% для правильного выравнивания */
  align-items: flex-end; /* Выравнивание по правому краю */
}

.todo-form {
  background-color: rgba(255, 255, 255, 0.6); /* Белый цвет с 80% непрозрачностью */
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 20px auto;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}


.todo-list {
  background-color: white;
  opacity: 0.6; /* 80% непрозрачности */
  border-radius: 10px;
  list-style-type: none;
  padding: 0;
  margin: 20px auto;
  max-width: 600px;

}


</style>
