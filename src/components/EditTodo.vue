<template>
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <div class="todo-edit">
    <div class="form-container">
      <h2>Редактировать задачу</h2>
      <form @submit.prevent="saveEdit" class="edit-form">
        <div class="input-container">
          <q-input v-model="todo.text" label="Название" outlined rounded class="q-mb-md todo-input-edit" id="text" />
          <q-input v-model="todo.description" label="Описание" outlined rounded autogrow class="q-mb-md todo-input-edit" id="description" />
          <q-input v-model="todo.country" label="Страна" outlined rounded class="q-mb-md todo-input-edit" id="country" />
          <q-input v-model="todo.city" label="Город" outlined rounded class="q-mb-md todo-input-edit" id="city" />
          <q-input v-model="todo.built" label="Дата постройки" outlined rounded class="q-mb-md todo-input-edit" id="built" />
          <q-input v-model="todo.coordinates" label="Координаты" outlined rounded class="q-mb-md todo-input-edit" id="coordinates" />
          <q-input v-model="todo.architect" label="Архитектор" outlined rounded class="q-mb-md todo-input-edit" id="architect" />
        </div>

        <q-select
            v-model="selectReligion"
            :options="filteredReligions"
            :label="selectReligion ? `Вы выбрали: ${selectReligion.name}` : `Текущая религия: ${todo.religion_name}`"
            option-label="name"
            option-value="id"
            use-input
            input-debounce="300"
            @filter="filterReligions"
            outlined
            rounded
            class="q-mb-md"
        >
          <template v-slot:append>
            <q-icon
                v-if="selectReligion != null"
                class="cursor-pointer custom-clear-icon"
                name="clear"
                @click.stop.prevent="clearSelection"
            />
          </template>
        </q-select>

        <div class="input-container1">
          <label for="file-upload">Добавить фото</label>
          <input type="file" id="file-upload" multiple @change="handleFileUpload" class="todo-input-file" />
        </div>

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

    <div class="todo-photos" v-if="todo.photos && todo.photos.length">
      <h3>Фотографии</h3>
      <div class="photos-gallery">
        <div v-for="(photo, index) in todo.photos" :key="photo.filename" class="photo-item">
          <img :src="'http://127.0.0.1:5000/' + photo.filepath" :alt="photo.filename" class="todo-photo" />
          <button class="delete-photo" @click="confirmDelete(index)">✖</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { QInput, QSelect, QIcon } from 'quasar';

const todo = ref({
  text: '',
  description: '',
  country: '',
  city: '',
  built: '',
  coordinates: '',
  architect: '',
  religion_id: '',  // Если религия не выбрана, это будет null
  religion_name: '', // Название религии (если есть)
  photos: [],
});

const files = ref([]);
const imagePreviews = ref([]);
const deletedPhotos = ref([]);
const religions = ref([]);
const route = useRoute();
const router = useRouter();
const selectReligion = ref(null); // Выбранная религия в списке
const filteredReligions = ref([]);

onMounted(async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/api/religions");
    religions.value = response.data;
    filteredReligions.value = religions.value;
  } catch (error) {
    console.error("Ошибка при загрузке религий:", error);
  }
});

onMounted(async () => {
  const todoId = route.params.id;
  try {
    const response = await axios.get(`http://127.0.0.1:5000/todo/${todoId}`);
    Object.assign(todo.value, response.data);
    const religionsResponse = await axios.get("http://127.0.0.1:5000/api/religions");
    religions.value = religionsResponse.data;
    if (todo.value.religion_id) {
      const religion = religions.value.find(rel => rel.id === todo.value.religion_id);
      selectReligion.value = religion;
    }
  } catch (error) {
    console.error('Ошибка при загрузке задачи:', error);
  }
});

const filterReligions = (val, update) => {
  update(() => {
    if (val) {
      const lowerVal = val.toLowerCase();
      filteredReligions.value = religions.value.filter((religion) =>
          religion.name.toLowerCase().includes(lowerVal)
      );
    } else {
      filteredReligions.value = religions.value;
    }
  });
};

function handleFileUpload(event) {
  const selectedFiles = Array.from(event.target.files);
  files.value.push(...selectedFiles);
  imagePreviews.value.push(...selectedFiles.map(file => URL.createObjectURL(file)));
}

function removePreviewImage(index) {
  imagePreviews.value.splice(index, 1);
  files.value.splice(index, 1);
}

function confirmDelete(index) {
  if (confirm('Вы уверены, что хотите удалить это фото?')) {
    deletePhoto(index);
  }
}

function deletePhoto(index) {
  const deletedPhoto = todo.value.photos[index];
  deletedPhotos.value.push(deletedPhoto);
  todo.value.photos.splice(index, 1);
}

const clearSelection = () => {
  selectReligion.value = null;
};

function validateForm() {
  if (!todo.value.text || !todo.value.description) {
    alert('Пожалуйста, заполните все обязательные поля.');
    return false;
  }
  return true;
}

async function saveEdit() {
  // Проверяем, прошла ли валидация формы
  if (!validateForm()) return;

  const todoId = route.params.id;  // Получаем ID задачи
  const formData = new FormData();

  // Если религия выбрана, отправляем её, если нет, отправляем старую религию
  if (selectReligion.value) {
    formData.append('religion_id', selectReligion.value.id);  // Новая религия
  } else if (todo.value.religion_id) {
    formData.append('religion_id', todo.value.religion_id);  // Старая религия (если она есть)
  }

  // Добавляем остальные данные задачи (кроме фотографий и религии)
  for (const [key, value] of Object.entries(todo.value)) {
    if (key !== 'photos' && key !== 'religion_name') {
      formData.append(key, value);  // Заполняем все поля, кроме религии
    }
  }

  // Добавляем фотографии, если они есть
  files.value.forEach((file) => {
    formData.append('photos', file);
  });

  // Добавляем уже существующие фотографии, если они есть
  todo.value.photos.forEach((photo) => {
    formData.append('existing_photos', photo.filename);
  });

  try {
    const response = await axios.put(`http://127.0.0.1:5000/api/todos/${todoId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    // Если задача была обновлена, перенаправляем на главную страницу
    if (response.data.message === 'Task updated successfully') {
      await deletePhotosFromDatabase(todoId);
      router.push('/');
    } else {
      alert('Произошла ошибка при сохранении задачи. Попробуйте снова.');
      console.error('Ошибка при сохранении задачи:', response.data);
    }
  } catch (error) {
    alert('Произошла ошибка при сохранении задачи. Попробуйте снова.');
    console.error('Ошибка при сохранении задачи:', error);
  }
}



async function deletePhotosFromDatabase(todoId) {
  try {
    for (const deletedPhoto of deletedPhotos.value) {
      await axios.delete(`http://127.0.0.1:5000/api/todos/${todoId}/photos/${deletedPhoto.filename}`);
    }
    deletedPhotos.value = [];
  } catch (error) {
    console.error('Ошибка при удалении фотографий с сервера:', error);
  }
}

function cancelEdit() {
  router.push('/');
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
  margin-bottom: 15px; /* Здесь вы можете настроить размер отступа */
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
