<template>
  <div class="todo-edit">
    <div class="form-container">
      <h2>Редактировать задачу</h2>
      <form @submit.prevent="saveEdit" class="edit-form">
        <div class="input-container">
          <label for="text">Текст задачи</label>
          <input v-model="todo.text" placeholder="Текст задачи" class="todo-input-edit" id="text">
        </div>
        <div class="input-container">
          <label for="country">Страна</label>
          <input v-model="todo.country" placeholder="Страна" class="todo-input-edit" id="country">
        </div>
        <div class="input-container">
          <label for="city">Город</label>
          <input v-model="todo.city" placeholder="Город" class="todo-input-edit" id="city">
        </div>
        <div class="input-container">
          <label for="built">Год постройки</label>
          <input v-model="todo.built" placeholder="Год постройки" class="todo-input-edit" id="built">
        </div>
        <div class="input-container">
          <label for="coordinates">Координаты</label>
          <input v-model="todo.coordinates" placeholder="Координаты" class="todo-input-edit" id="coordinates">
        </div>
        <div class="input-container">
          <label for="architect">Архитектор</label>
          <input v-model="todo.architect" placeholder="Архитектор" class="todo-input-edit" id="architect">
        </div>
        <div class="input-container">
          <label for="relig">Религия</label>
          <input v-model="todo.relig" placeholder="Религия" class="todo-input-edit" id="relig">
        </div>

        <button type="submit" class="save-button">Сохранить</button>
      </form>
      <button @click="cancelEdit" class="cancel-button">Отменить</button>
    </div>

    <!-- Контейнер для отображения фотографий -->
    <div class="todo-photos" v-if="todo.photos && todo.photos.length">
      <h3>Фотографии</h3>
      <div class="photos-gallery">
        <div v-for="(photo, index) in todo.photos" :key="photo.filename" class="photo-item">
          <img :src="'http://127.0.0.1:5000/' + photo.filepath" :alt="photo.filename" class="todo-photo" />
          <!-- Кнопка для удаления фото -->
          <button class="delete-photo" @click="deletePhoto(index)">
            ✖
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const todo = ref({
  text: '',
  country: '',
  city: '',
  built: '',
  coordinates: '',
  architect: '',
  relig: '',
  photos: []  // Массив для фото
})
const route = useRoute()
const router = useRouter()

// Загружаем данные задачи при монтировании компонента
onMounted(async () => {
  const todoId = route.params.id
  try {
    const response = await axios.get(`http://127.0.0.1:5000/todo/${todoId}`)
    Object.assign(todo.value, response.data)
  } catch (error) {
    console.error('Ошибка при загрузке задачи:', error)
  }
})

// Функция для удаления фото
async function deletePhoto(index) {
  const photoFilename = todo.value.photos[index].filename;  // Получаем только имя файла
  try {
    const response = await axios.delete(`http://127.0.0.1:5000/api/todos/${route.params.id}/photos/${photoFilename}`);
    console.log('Ответ сервера на удаление:', response.data);  // Логируем ответ

    if (response.data.message === 'Photo deleted successfully') {
      todo.value.photos.splice(index, 1);  // Удаляем фото из массива
    }
  } catch (error) {
    console.error('Ошибка при удалении фото:', error);
  }
}



// Сохраняем изменения
async function saveEdit() {
  const todoId = route.params.id
  try {
    const response = await axios.put(`http://127.0.0.1:5000/api/todos/${todoId}`, todo.value)
    if (response.data.message === 'Task updated successfully') {
      router.push('/')  // Перенаправление на главную страницу после сохранения
    }
  } catch (error) {
    console.error('Ошибка при сохранении задачи:', error)
  }
}

// Отмена редактирования
function cancelEdit() {
  router.push('/')  // Перенаправление на главную страницу
}
</script>


<style scoped>

/* Стили для крестика на фото */
.delete-photo {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  border-radius: 50%;
  width: 25px;
  height: 25px;
  font-size: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  opacity: 0.8;
  transition: opacity 0.3s;
}

.delete-photo:hover {
  opacity: 1;
}

/* Обновленный стиль для фотографий */
.photo-item {
  position: relative;
  width: 100%;
  max-width: 200px; /* Ограничиваем максимальную ширину */
  height: 200px; /* Фиксированная высота */
  margin-bottom: 10px;
}

.todo-photo {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}


.todo-edit {
  display: flex;
  justify-content: space-between;
  max-width: 1200px;
  width: 90%;
  margin: 30px auto;
  padding: 30px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-container {
  width: 60%; /* Контейнер формы будет занимать 60% ширины */
}

.input-container {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px; /* Добавим отступы между полями формы */
}

label {
  margin-bottom: 5px;
  font-weight: bold;
  font-size: 14px;
  color: #555;
}

.todo-input-edit {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s;
}

.todo-input-edit:focus {
  border-color: #4caf50;
}

.save-button {
  padding: 15px 25px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  margin-top: 20px;
}

.save-button:hover {
  background-color: #388e3c;
}

.cancel-button {
  padding: 15px 25px;
  background-color: #777373;
  color: white;
  border: none;
  margin-top: 20px;
  border-radius: 50px;
  cursor: pointer;
}

.cancel-button:hover {
  background-color: #b72121;
}

/* Контейнер для фотографий */
.todo-photos {
  width: 35%;  /* Контейнер с фотографиями занимает 35% ширины */
  margin-top: 30px;  /* Добавим отступ сверху для фотографий */
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  overflow: hidden; /* Скрывает все, что выходит за пределы контейнера */
}

.photos-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;  /* Расстояние между фотографиями */
  justify-content: center;
}

.todo-photo {
  width: 100%;
  max-width: 200px;  /* Ограничиваем максимальную ширину фотографии */
  height: 200px;  /* Фиксированная высота для квадратного формата */
  object-fit: contain;  /* Изображение будет сжиматься, чтобы поместиться в квадратный контейнер */
  border-radius: 10px;  /* Закругление углов фотографий */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);  /* Легкая тень для фотографии */
}


</style>
