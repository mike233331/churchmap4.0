<template>
  <div>
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
        <p><strong>Religion:</strong> {{ todo.religion_name }}</p>
      </div>

      <div v-if="todo.photos?.length" class="todo-photos">
        <q-carousel v-model="slide" swipeable animated thumbnails infinite>
          <q-carousel-slide
              v-for="(photo, index) in todo.photos"
              :key="photo.filename"
              :name="index + 1"
              :img-src="`http://127.0.0.1:5000/uploads/${photo.filename}`"
              @click="openModal(`http://127.0.0.1:5000/uploads/${photo.filename}`)"
          />
        </q-carousel>
      </div>
    </div>

    <div v-if="isModalOpen" class="modal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <img :src="modalImage" alt="Фото" class="modal-image" />
      </div>
    </div>


  </div>
</template>



<script>
import { defineComponent, ref } from "vue";
import { QCarousel, QCarouselSlide } from "quasar";
import axios from "axios";

export default defineComponent({
  name: "TodoView",
  components: { QCarousel, QCarouselSlide },
  data() {
    return {
      todo: null,
      slide: ref(1),
      isModalOpen: false,
      modalImage: "",
    };
  },
  created() {
    axios
        .get(`http://127.0.0.1:5000/todo/${this.$route.params.id}`)
        .then((response) => (this.todo = response.data))
        .catch((error) => console.error("Error fetching todo:", error));
  },
  methods: {
    openModal(imageSrc) {
      this.modalImage = imageSrc;
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
      this.modalImage = "";
    },
  },
});
</script>



<style scoped>
  /* Стили для кнопки "Назад" */
  .back-button {
    position: fixed; /* Фиксируем кнопку вне контейнера */
    top: 20px; /* Расстояние от верхней части экрана */
    left: 50%; /* Центрируем кнопку по горизонтали */
    transform: translateX(-50%); /* Корректируем центрирование */
    z-index: 10; /* Поверх всех элементов */
    width: 100%; /* Ширина кнопки */
    text-align: center; /* Выравниваем текст по центру */
  }

  .back-button button {
    padding: 12px;
    width: 50%; /* Устанавливаем ширину кнопки */
    background-color: #80cbc4;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .back-button button:hover {
    background-color: #4db6ac; /* Более темный оттенок при наведении */
  }

.todo-container {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
  padding: 20px;
  max-width: 600px;
  margin: 20px auto; /* Уменьшили отступ сверху */
  background: #e0f7fa; /* Бирюзовый фон */
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: relative; /* Для управления позиционированием */
  top: 0; /* Убираем любое смещение вниз */
  transform: translateY(-20px); /* Поднимаем контейнер выше */
}

.todo-title {
  font-size: 2rem;
  font-weight: bold;
  color: #00796b;
  margin-bottom: 20px;
  text-align: center;
}

.todo-details p {
  font-size: 1.1rem;
  margin: 10px 0;
}

.todo-details strong {
  color: #004d40;
}

.todo-not-found {
  text-align: center;
  font-size: 1.5rem;
  color: #e74c3c;
  margin-top: 50px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  overflow: hidden;
}

.modal-content {
  max-width: 90%;
  max-height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 8px;
}
</style>
