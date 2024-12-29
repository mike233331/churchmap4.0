<template>
  <div class="todo-edit">
    <div class="form-container">
      <h2>Редактировать задачу</h2>
      <form @submit.prevent="saveEdit" class="edit-form">
        <!-- Поля формы для редактирования задачи -->
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

        <div class="custom-select" ref="dropdownContainer">
          <label for="relig">Религия</label>
          <input
              type="text"
              v-model="selectedReligionName"
              :placeholder="todo.religion_id ? `Religion: ${todo.religion_id}` : 'Поиск религии...'"
              @click="toggleDropdown"
              @input="filterReligions"
              class="todo-input-edit"
          />
          <ul v-if="isDropdownOpen" class="dropdown-menu">
            <li
                v-for="(religionItem, index) in filteredReligions"
                :key="index"
                @click="selectReligion(religionItem)"
                class="dropdown-item"
            >
              {{ religionItem.name }}
            </li>
          </ul>
        </div>




        <!-- Загрузка новых фото -->
        <div class="input-container1">
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
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const todo = ref({
  text: '',
  country: '',
  city: '',
  built: '',
  coordinates: '',
  architect: '',
  religion_id: null,
  photos: [],
});

const files = ref([]); // Новые загружаемые файлы
const imagePreviews = ref([]); // Предпросмотры новых фото
const deletedPhotos = ref([]); // Массив для хранения удалённых фото

const religions = ref([]);
const searchQuery = ref("");
const selectedReligionName = ref("");
const isDropdownOpen = ref(false);

const route = useRoute();
const router = useRouter();

// Загружаем данные задачи и религии
onMounted(async () => {
  const todoId = route.params.id;
  try {
    const response = await axios.get(`http://127.0.0.1:5000/todo/${todoId}`);
    Object.assign(todo.value, response.data);

    // Загружаем религии
    const religionsResponse = await axios.get("http://127.0.0.1:5000/api/religions");
    religions.value = religionsResponse.data;

    if (todo.value.religion_id) {
      const religion = religions.value.find(rel => rel.id === todo.value.religion_id);
      selectedReligionName.value = religion ? religion.name : "";
    }
  } catch (error) {
    console.error('Ошибка при загрузке задачи:', error);
  }
});

// Отфильтрованный список религий
const filteredReligions = computed(() =>
    religions.value.filter((rel) =>
        rel.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
);

// Управление выпадающим списком религий
function toggleDropdown() {
  isDropdownOpen.value = !isDropdownOpen.value;
}

function filterReligions() {
  isDropdownOpen.value = true;
}

// Выбор религии
function selectReligion(selectedReligion) {
  todo.value.religion_id = selectedReligion.id;
  selectedReligionName.value = selectedReligion.name;
  isDropdownOpen.value = false;
}

// Обработка загрузки новых фото
function handleFileUpload(event) {
  const selectedFiles = Array.from(event.target.files);
  files.value.push(...selectedFiles);
  imagePreviews.value.push(...selectedFiles.map(file => URL.createObjectURL(file)));
}

// Удаление изображения из предпросмотра
function removePreviewImage(index) {
  imagePreviews.value.splice(index, 1);
  files.value.splice(index, 1); // Удаляем файл из массива файлов
}

// Удаление существующего фото
function deletePhoto(index) {
  const deletedPhoto = todo.value.photos[index];
  deletedPhotos.value.push(deletedPhoto);
  todo.value.photos.splice(index, 1);
}

// Сохранение изменений, включая новые фото и удалённые фото
async function saveEdit() {
  const todoId = route.params.id;
  const formData = new FormData();

  // Добавляем текстовые данные
  for (const [key, value] of Object.entries(todo.value)) {
    if (key !== 'photos') {
      formData.append(key, value);
    }
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
      // Отправляем информацию о удалённых фотографиях
      await deletePhotosFromDatabase(todoId);
      router.push('/'); // Перенаправление после сохранения
    } else {
      console.error('Ошибка при сохранении задачи:', response.data);
    }
  } catch (error) {
    console.error('Ошибка при сохранении задачи:', error);
  }
}


// Отправка данных о удалённых фото на сервер
async function deletePhotosFromDatabase(todoId) {
  try {
    for (const deletedPhoto of deletedPhotos.value) {
      await axios.delete(`http://127.0.0.1:5000/api/todos/${todoId}/photos/${deletedPhoto.filename}`);
    }
    deletedPhotos.value = []; // Очищаем массив удалённых фотографий
  } catch (error) {
    console.error('Ошибка при удалении фотографий с сервера:', error);
  }
}

// Отмена редактирования
function cancelEdit() {
  router.push('/'); // Перенаправление на главную страницу
}
</script>





<style scoped>
.input-container {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px; /* Отступы между полями формы */
}

label {
  margin-bottom: 5px;
  font-weight: bold;
  font-size: 14px;
  color: #555;
}

.todo-input-edit, .custom-select select {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 16px;
  outline: none;
  width: 100%; /* Для выравнивания */
  transition: border-color 0.3s;
}

.todo-input-edit:focus, .custom-select select:focus {
  border-color: #4caf50;
}

.custom-select {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  background: white;
  border: 1px solid #ddd;
  border-radius: 20px;
  max-height: 200px;
  overflow-y: auto;
  list-style: none;
  padding: 0;
  margin: 0;
  z-index: 1000;
  width: 100%;
}

.dropdown-item {
  padding: 10px 15px;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #f0f0f0;
}

/* Стили для фотографий */
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

/* Стили для кнопки сохранения */
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

/* Стили для поля загрузки файла */
.input-container1 input[type="file"] {
  display: none; /* Скрываем стандартное поле загрузки */
}

/* Стиль для кнопки загрузки фото */
.input-container1 label[for="file-upload"] {
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

/* Стили для формы */
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

.custom-select {
  position: relative;
}

.custom-select select {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 16px;
  outline: none;
  width: 100%;
  transition: border-color 0.3s;
}

.custom-select select:focus {
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

/* Отступ между полем с религией и полем для фото */
.input-container1 {
  margin-top: 40px; /* Увеличили отступ между полями */
}
</style>
