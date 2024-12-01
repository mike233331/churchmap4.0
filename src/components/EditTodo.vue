<template>
  <div class="todo-edit">
    <div class="form-container">
      <h2>Редактировать задачу</h2>
      <form @submit.prevent="saveEdit" class="edit-form">
        <div class="input-container">
          <label for="text">Текст задачи</label>
          <input v-model="todo.text" placeholder="Текст задачи" class="todo-input-edit" id="text" />
        </div>
        <div class="input-container">
          <label for="country">Страна</label>
          <input v-model="todo.country" placeholder="Страна" class="todo-input-edit" id="country" />
        </div>
        <div class="input-container">
          <label for="city">Город</label>
          <input v-model="todo.city" placeholder="Город" class="todo-input-edit" id="city" />
        </div>
        <div class="input-container">
          <label for="built">Год постройки</label>
          <input v-model="todo.built" placeholder="Год постройки" class="todo-input-edit" id="built" />
        </div>
        <div class="input-container">
          <label for="coordinates">Координаты</label>
          <input v-model="todo.coordinates" placeholder="Координаты" class="todo-input-edit" id="coordinates" />
        </div>
        <div class="input-container">
          <label for="architect">Архитектор</label>
          <input v-model="todo.architect" placeholder="Архитектор" class="todo-input-edit" id="architect" />
        </div>
        <div class="input-container">
          <label for="relig">Религия</label>
          <input v-model="todo.relig" placeholder="Религия" class="todo-input-edit" id="relig" />
        </div>

        <!-- Загрузка новых фото -->
        <div class="input-container">
          <label for="file-upload">Добавить фото</label>
          <input type="file" id="file-upload" multiple @change="handleFileUpload" class="todo-input-file" />
        </div>

        <!-- Предпросмотр новых фото -->
        <div v-if="imagePreviews.length > 0" class="image-previews">
          <div v-for="(preview, index) in imagePreviews" :key="index" class="image-preview">
            <img :src="preview" alt="Предпросмотр изображения" class="preview-image" />
            <button @click="removePreviewImage(index)" class="remove-image-btn">X</button>
          </div>
        </div>

        <button type="submit" class="save-button">Сохранить</button>
      </form>
      <button @click="cancelEdit" class="cancel-button">Отменить</button>
    </div>

    <!-- Контейнер для отображения существующих фотографий -->
    <div class="todo-photos" v-if="todo.photos && todo.photos.length">
      <h3>Фотографии</h3>
      <div class="photos-gallery">
        <div v-for="(photo, index) in todo.photos" :key="photo.filename" class="photo-item">
          <img :src="'http://127.0.0.1:5000/' + photo.filepath" :alt="photo.filename" class="todo-photo" />
          <button class="delete-photo" @click="deletePhoto(index)">✖</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const todo = ref({
  text: '',
  country: '',
  city: '',
  built: '',
  coordinates: '',
  architect: '',
  relig: '',
  photos: [], // Массив для существующих фото
});
const files = ref([]); // Новые загружаемые файлы
const imagePreviews = ref([]); // Предпросмотры новых фото
const route = useRoute();
const router = useRouter();

// Загружаем данные задачи при монтировании компонента
onMounted(async () => {
  const todoId = route.params.id;
  try {
    const response = await axios.get(`http://127.0.0.1:5000/todo/${todoId}`);
    Object.assign(todo.value, response.data);
  } catch (error) {
    console.error('Ошибка при загрузке задачи:', error);
  }
});

// Обработка загрузки новых фото
function handleFileUpload(event) {
  const selectedFiles = Array.from(event.target.files);
  files.value.push(...selectedFiles);
  imagePreviews.value.push(...selectedFiles.map(file => URL.createObjectURL(file)));
}

// Удаление фото из предпросмотра
function removePreviewImage(index) {
  imagePreviews.value.splice(index, 1);
  files.value.splice(index, 1);
}

// Удаление существующего фото
async function deletePhoto(index) {
  const photoFilename = todo.value.photos[index].filename;
  try {
    const response = await axios.delete(`http://127.0.0.1:5000/api/todos/${route.params.id}/photos/${photoFilename}`);
    if (response.data.message === 'Photo deleted successfully') {
      todo.value.photos.splice(index, 1);
    }
  } catch (error) {
    console.error('Ошибка при удалении фото:', error);
  }
}

// Сохранение изменений, включая новые фото
async function saveEdit() {
  console.log('Отправка данных для сохранения...');
  const todoId = route.params.id;
  const formData = new FormData();

  // Добавляем текстовые данные
  for (const [key, value] of Object.entries(todo.value)) {
    if (key !== 'photos') formData.append(key, value);
  }

  // Добавляем новые фото
  files.value.forEach(file => {
    formData.append('photos', file);
  });

  try {
    const response = await axios.put(`http://127.0.0.1:5000/api/todos/${todoId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    if (response.data.message === 'Task updated successfully') {
      console.log('Задача успешно обновлена');
      router.push('/'); // Перенаправление после сохранения
    } else {
      console.error('Ошибка при сохранении задачи:', response.data);
    }
  } catch (error) {
    console.error('Ошибка при сохранении задачи:', error);
  }
}

// Отмена редактирования
function cancelEdit() {
  router.push('/'); // Перенаправление на главную страницу
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


/* Стили для поля загрузки файла */
.input-container input[type="file"] {
  display: none; /* Скрываем стандартное поле загрузки */
}

/* Стиль для кнопки загрузки фото */
.input-container label[for="file-upload"] {
  display: inline-block;
  padding: 12px 20px;
  background-color: #4caf50;
  color: white;
  border-radius: 50px;
  cursor: pointer;
  font-size: 16px;
  text-align: center;
  transition: background-color 0.3s;
}

.input-container label[for="file-upload"]:hover {
  background-color: #388e3c;
}

/* Стиль для предпросмотра изображений */
.image-previews {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}

.image-preview {
  position: relative;
  width: 100px;
  height: 100px;
  margin-bottom: 10px;
  border-radius: 10px;
  overflow: hidden;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.remove-image-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: rgba(255, 0, 0, 0.7);
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  opacity: 0.8;
  transition: opacity 0.3s;
}

.remove-image-btn:hover {
  opacity: 1;
}

/* Стили для контейнера фотографий */
.todo-photos {
  width: 35%;
  margin-top: 30px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* Стили для фотографий в галерее */
.photos-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: center;
}

.photo-item {
  position: relative;
  width: 100%;
  max-width: 200px;
  height: 200px;
  margin-bottom: 10px;
  border-radius: 10px;
  overflow: hidden;
}

.todo-photo {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

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


</style>