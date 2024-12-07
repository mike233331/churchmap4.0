<template>
  <div>
    <!-- Кнопка для возвращения на главную страницу -->
    <router-link to="/" class="back-button">
      <button>Назад</button>
    </router-link>

    <div class="todo-container" v-if="todo">
      <h1 class="todo-title">{{ todo.text }}</h1>
      <div class="todo-details">
        <p><strong>Country:</strong> {{ todo.country }}</p>
        <p><strong>City:</strong> {{ todo.city }}</p>
        <p><strong>Built Year:</strong> {{ todo.built }}</p>
        <p><strong>Coordinates:</strong> {{ todo.coordinates }}</p>
        <p><strong>Architect:</strong> {{ todo.architect }}</p>
        <p><strong>Religion:</strong> {{ todo.relig }}</p>
      </div>

      <!-- Отображение фотографий -->
      <div class="todo-photos" v-if="todo.photos && todo.photos.length">
        <h3>Фотографии</h3>
        <div class="photos-gallery">
          <img
              v-for="photo in todo.photos"
              :key="photo.filename"
              :src="'http://127.0.0.1:5000/' + photo.filepath"
              :alt="photo.filename"
              class="todo-photo"
              @click="openModal('http://127.0.0.1:5000/' + photo.filepath)" />
        </div>
      </div>
    </div>

    <div v-else class="todo-not-found">
      <p>Todo not found.</p>
    </div>

    <!-- Модальное окно для отображения изображения в полном размере -->
    <div v-if="isModalOpen" class="modal" @click.self="closeModal">
      <img :src="modalImage" class="modal-image" />
    </div>
  </div>
</template>


<script>
import axios from "axios";

export default {
  data() {
    return {
      todo: null, // Сюда будут загружены данные todo
      isModalOpen: false, // Статус модального окна
      modalImage: "", // URL для отображаемого изображения в модальном окне
    };
  },
  created() {
    const id = this.$route.params.id; // Получаем ID из маршрута
    axios
        .get(`http://127.0.0.1:5000/todo/${id}`)
        .then((response) => {
          this.todo = response.data; // Сохраняем данные todo
        })
        .catch((error) => {
          console.error("Error fetching todo:", error);
        });
  },
  methods: {
    openModal(imageSrc) {
      this.modalImage = imageSrc; // Устанавливаем URL изображения в модальном окне
      this.isModalOpen = true; // Открываем модальное окно
    },
    closeModal() {
      this.isModalOpen = false; // Закрываем модальное окно
      this.modalImage = ""; // Очищаем URL изображения
    }
  }
};
</script>


<style scoped>
/* Стили для кнопки "Назад" */
.back-button {
  display: block;
  margin: 20px auto;
  width: 100%;
  text-align: center;
}

.back-button button {
  padding: 12px;
  width: 47%;
  background-color: #80cbc4; /* Более приглушенный бирюзовый */
  color: #ffffff;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.back-button button:hover {
  background-color: #4db6ac; /* Более темный оттенок при наведении */
}

/* Добавление бирюзового фона */
.todo-container {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
  padding: 20px;
  max-width: 600px;
  margin: 40px auto;
  background: #e0f7fa; /* Бирюзовый фон */
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.todo-title {
  font-size: 2rem;
  font-weight: bold;
  color: #00796b; /* Темно-бирюзовый цвет для заголовка */
  margin-bottom: 20px;
  text-align: center;
}

.todo-details p {
  font-size: 1.1rem;
  margin: 10px 0;
}

.todo-details strong {
  color: #004d40; /* Темный акцент для ключевых слов */
}

.todo-not-found {
  text-align: center;
  font-size: 1.5rem;
  color: #e74c3c;
  margin-top: 50px;
}

/* Стили для блока с фотографиями */
.todo-photos {
  margin-top: 30px;
}

.photos-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.todo-photo {
  width: 300px; /* Фиксированная ширина */
  height: 200px; /* Фиксированная высота */
  object-fit: contain; /* Изображение будет полностью видно, сжато по необходимости */
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  cursor: pointer; /* Курсор меняется на указатель при наведении */
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
  object-fit: contain; /* Изображение не будет искажаться */
}
</style>

