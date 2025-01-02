<template>
  <div>
    <router-link to="/" class="back-button">
      <button>Назад</button>
    </router-link>

    <div class="todo-container" v-if="todo">
      <h1 class="todo-title">{{ todo.text }}</h1>
      <div class="todo-details">
        <p>
          <strong>Description:</strong> <span>{{ truncatedDescription }}<span v-if="isDescriptionTruncated" class="read-more" @click="showFullDescription" style="font-size: 0.8rem; color: #1a6daf;"> ... (read more)</span></span>
        </p>
        <p><strong>Country:</strong> <span>{{ todo.country }}</span></p>
        <p><strong>City:</strong> <span>{{ todo.city }}</span></p>
        <p><strong>Built Year:</strong> <span>{{ todo.built }}</span></p>
        <p><strong>Coordinates:</strong> <span>{{ todo.coordinates }}</span></p>
        <p><strong>Architect:</strong> <span>{{ todo.architect }}</span></p>
        <p><strong>Religion:</strong> <span>{{ todo.religion_name }}</span></p>
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

    <div v-if="isDescriptionModalOpen" class="modal" @click="closeDescriptionModal">
      <div class="modal-content" @click.stop>
        <p>{{ todo.description }}</p>
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
      isDescriptionModalOpen: false,
      truncatedDescriptionLength: 20,
    };
  },
  computed: {
    isDescriptionTruncated() {
      return (
          this.todo &&
          this.todo.description &&
          this.todo.description.length > this.truncatedDescriptionLength
      );
    },
    truncatedDescription() {
      return this.isDescriptionTruncated
          ? this.todo.description.slice(0, this.truncatedDescriptionLength)
          : this.todo.description;
    },
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
    showFullDescription() {
      this.isDescriptionModalOpen = true;
    },
    closeDescriptionModal() {
      this.isDescriptionModalOpen = false;
    },
  },
});

</script>

<style scoped>
/* Стили для кнопки "Назад" */
.back-button {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  width: 100%;
  text-align: center;
}

.back-button button {
  padding: 12px;
  width: 50%;
  background-color: #80cbc4;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-button button:hover {
  background-color: #4db6ac;
}

.todo-container {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
  padding: 20px;
  max-width: 600px;
  margin: 20px auto;
  background: #e0f7fa;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: relative;
  top: 0;
  transform: translateY(-20px);
}

.todo-title {
  font-size: 2rem;
  font-weight: bold;
  color: #00718F;
  margin-bottom: 20px;
  text-align: center;
}

.todo-details {
  display: grid;
  gap: 5px 15px;
  align-items: center;
  justify-items: start;
}

.todo-details p {
  margin: 2px;
}

.todo-details strong {
  font-size: 1.3rem; /* Можно оставить, чтобы чуть увеличить размер */
  color: #0BA5BE;
  font-weight: 900; /* Устанавливаем максимальную жирность */
  text-align: left;
}



.todo-details span {
  font-size: 1.1rem;
  color: #2c3e50;
}

.read-more {
  font-size: 0.8rem;
  cursor: pointer;
  font-weight: bold;
  text-decoration: underline;

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
  width: 40%;
  height: 50%;
  max-width: 80%;
  max-height: 50%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 20px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  color: #2c3e50;
  font-size: 1.2rem;
  line-height: 1.6;
  overflow: auto;
  word-break: break-word;
  white-space: normal;
}


.modal-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 8px;
}
</style>
