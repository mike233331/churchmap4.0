<template>
  <div class="todo-add">
    <form @submit.prevent="addTodo" class="todo-form" enctype="multipart/form-data">
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

        <!-- Кнопка загрузки файлов -->
        <label for="file-upload" class="todo-file-upload-label">Добавить файлы</label>
        <input type="file" id="file-upload" multiple @change="handleFileUpload" class="todo-input todo-file-upload" />

        <!-- Предпросмотр изображений -->
        <div v-if="imagePreviews.length > 0" class="image-previews">
          <div v-for="(preview, index) in imagePreviews" :key="index" class="image-preview">
            <img :src="preview" alt="Предпросмотр изображения" class="preview-image" @click="openImage(preview)" />
            <button @click="removeImage(index)" class="remove-image-btn">X</button>
          </div>
        </div>

        <button class="todo-button">Добавить</button>
      </div>
    </form>

    <!-- Модальное окно для просмотра фото -->
    <div v-if="isModalOpen" class="modal" @click.self="closeModal">
      <img :src="modalImage" class="modal-image" />
    </div>
  </div>
</template>


<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const title = ref('');
const country = ref('');
const architect = ref('');
const city = ref('');
const built = ref('');
const religion = ref('');
const coordinates = ref('');
const files = ref([]); // Список файлов
const imagePreviews = ref([]); // Массив для хранения URL предпросмотра изображений
const isModalOpen = ref(false); // Статус модального окна
const modalImage = ref(''); // URL для отображаемого изображения в модальном окне
const router = useRouter();

function handleFileUpload(event) {
  const selectedFiles = event.target.files;
  files.value = Array.from(selectedFiles); // Преобразуем в массив

  // Создание URL для предпросмотра изображений
  imagePreviews.value = Array.from(selectedFiles).map(file => URL.createObjectURL(file));
}

function removeImage(index) {
  // Удаление изображения из массива предпросмотра
  imagePreviews.value.splice(index, 1);

  // Удаление файла из списка файлов
  files.value.splice(index, 1); // Мы удаляем файл по индексу
}

function openImage(imageSrc) {
  modalImage.value = imageSrc;
  isModalOpen.value = true;
}

function closeModal() {
  isModalOpen.value = false;
  modalImage.value = '';
}

async function addTodo() {
  try {
    const formData = new FormData();
    formData.append('text', title.value);
    formData.append('country', country.value);
    formData.append('city', city.value);
    formData.append('built', built.value);
    formData.append('coordinates', coordinates.value);
    formData.append('architect', architect.value);
    formData.append('relig', religion.value);

    // Добавляем файлы в formData
    Array.from(files.value).forEach(file => {
      formData.append('photos', file);
    });

    await axios.post('http://127.0.0.1:5000/api/todos', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    router.push('/'); // Перенаправление после добавления
  } catch (error) {
    console.error('Ошибка при добавлении задачи:', error);
  }
}
</script>



<style scoped>
/* Общие стили для формы добавления задачи */
.todo-add {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: white;
  opacity: 0.91; /* Полупрозрачный фон */
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  box-sizing: border-box; /* Чтобы padding и border не выходили за пределы контейнера */
}

.todo-form {
  display: flex;
  flex-wrap: wrap; /* Чтобы элементы не выходили за пределы */
  gap: 20px;
  box-sizing: border-box;
}

.column-left,
.column-right {
  display: flex;
  flex-direction: column;
  width: 48%; /* Два столбца, чтобы форма была аккуратной */
  box-sizing: border-box; /* Чтобы поля ввода не выходили за пределы */
}

.todo-input {
  width: 100%;
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #b2dfdb;
  border-radius: 5px;
  background-color: #f0f8ff;
  font-size: 14px;
  color: #00796b;
  box-sizing: border-box; /* Чтобы поля не выходили за пределы */
}

.todo-input:focus {
  border-color: #00796b;
  background-color: #e0f7fa;
}

.todo-button {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: 1px solid #b2dfdb;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 10px;
  width: 100%; /* Кнопка будет растягиваться на всю ширину родительского контейнера */
  box-sizing: border-box; /* Учитывает padding и border в расчете ширины */
}

.todo-button:hover {
  background-color: #388e3c;
}

/* Стили для кнопки загрузки файлов */
.todo-file-upload {
  display: none; /* Скрыть стандартное поле ввода файлов */
}

.todo-file-upload-label {
  display: inline-block;
  padding: 10px 20px;
  background-color: #2196f3;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  font-size: 13px;
  margin-top: 5.5px;
  width: 100%;
  text-align: center;
  box-sizing: border-box;
}

.todo-file-upload-label:hover {
  background-color: #1976d2;
}

/* Стили для предпросмотра изображений */
.image-previews {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.image-preview {
  position: relative;
  width: 100px;
  height: 100px;
  overflow: hidden;
  border-radius: 5px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background: rgba(255, 0, 0, 0.7);
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  cursor: pointer;
  font-size: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.remove-image-btn:hover {
  background: red;
}

/* Стили для модального окна */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-image {
  max-width: 90%;
  max-height: 90%;
  border-radius: 10px;
}
</style>
