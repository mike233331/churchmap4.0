<template>
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <div class="todo-add">
    <form @submit.prevent="addTodo" class="todo-form" enctype="multipart/form-data">
      <div class="column-right">
        <q-input v-model="title" label="Добавьте название" required :minlength="3" :maxlength="100" outlined rounded class="q-mb-md" />
        <q-input v-model="country" label="Добавьте страну" required :minlength="3" :maxlength="50" outlined rounded class="q-mb-md" />
        <q-input v-model="architect" label="Добавьте имя архитектора" required :minlength="3" :maxlength="50" outlined rounded class="q-mb-md" />
        <q-input v-model="city" label="Добавьте город" required :minlength="3" :maxlength="50" outlined rounded class="q-mb-md" />
      </div>

      <div class="column-left">
        <q-input v-model="built" label="Добавьте дату строительства" required :minlength="4" :maxlength="4" outlined rounded class="q-mb-md" />

        <q-select
            v-model="selectReligion"
            :options="filteredReligions"
            label="Выберите религию"
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
            <!-- Кнопка для очистки выбранного значения -->
            <q-icon
                v-if="selectReligion != null"
                class="cursor-pointer custom-clear-icon"
                name="clear"
                @click.stop.prevent="clearSelection"
            />
          </template>
        </q-select>

        <q-input v-model="coordinates" label="Добавьте координаты" required :minlength="5" :maxlength="50" outlined rounded class="q-mb-md" />

        <q-btn style="width: 100%; height: 56px;" unelevated rounded  label="Добавить файлы" @click="triggerFileInput" class="todo-file-upload q-mb-md animated-button" />

        <input type="file" id="file-upload" multiple ref="fileInput" @change="handleFileUpload" style="display: none" />

        <div v-if="imagePreviews.length" class="image-previews">
          <div v-for="(preview, index) in imagePreviews" :key="index" class="image-preview">
            <img :src="preview" alt="Предпросмотр изображения" class="preview-image" @click="openImage(preview)" />
            <button @click="removeImage(index)" class="remove-image-btn">X</button>
          </div>
        </div>

        <!-- Кнопка отправки формы -->
      </div>
    </form>

    <div v-if="isModalOpen" class="modal" @click.self="closeModal">
      <img :src="modalImage" class="modal-image" />
    </div>
    <form @submit.prevent="addTodo" class="todo-form" enctype="multipart/form-data">
      <!-- Остальные поля формы -->

      <q-btn label="Добавить задачу" type="submit" unelevated rounded class="q-mb-md animated-button" style="width: 100%; height: 56px;" />
    </form>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { QInput, QBtn, QSelect, QIcon } from 'quasar'; // Импорт компонентов Quasar

// Ссылки на данные формы
const title = ref("");
const country = ref("");
const architect = ref("");
const city = ref("");
const built = ref("");
const coordinates = ref("");
const files = ref([]); // Список файлов
const imagePreviews = ref([]); // Массив для хранения URL предпросмотра изображений
const isModalOpen = ref(false); // Статус модального окна
const modalImage = ref(""); // URL для отображаемого изображения в модальном окне
const router = useRouter();
const selectReligion = ref(null); // Модель для выбранной религии
const religions = ref([]); // Данные о религиях из базы данных
const filteredReligions = ref([]); // Отфильтрованные религии

// Загружаем религии при монтировании компонента
onMounted(async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/api/religions");
    religions.value = response.data;  // Получаем религии из базы данных
    filteredReligions.value = religions.value; // Инициализируем список религий
  } catch (error) {
    console.error("Ошибка при загрузке религий:", error);
  }
});

// Функция для фильтрации религий
const filterReligions = (val, update) => {
  update(() => {
    if (val) {
      // Если есть введенный текст, фильтруем
      const lowerVal = val.toLowerCase();
      filteredReligions.value = religions.value.filter((religion) =>
          religion.name.toLowerCase().includes(lowerVal)
      );
    } else {
      // Если текста нет, показываем все религии
      filteredReligions.value = religions.value;
    }
  });
};

// Функция для очистки выбранной религии
const clearSelection = () => {
  selectReligion.value = null;
};

// Работа с изображениями
function handleFileUpload(event) {
  const selectedFiles = event.target.files;
  files.value = Array.from(selectedFiles); // Преобразуем в массив
  imagePreviews.value = Array.from(selectedFiles).map((file) =>
      URL.createObjectURL(file)
  );
}

function removeImage(index) {
  imagePreviews.value.splice(index, 1);
  files.value.splice(index, 1);
}

function openImage(imageSrc) {
  modalImage.value = imageSrc;
  isModalOpen.value = true;
}

function closeModal() {
  isModalOpen.value = false;
  modalImage.value = "";
}

// Отправка формы
async function addTodo() {
  try {
    const formData = new FormData();
    formData.append("text", title.value);
    formData.append("country", country.value);
    formData.append("city", city.value);
    formData.append("built", built.value);
    formData.append("coordinates", coordinates.value);
    formData.append("architect", architect.value);
    formData.append("religion_id", selectReligion.value ? selectReligion.value.id : null); // Отправляем только ID

    // Добавление всех файлов
    Array.from(files.value).forEach((file) => {
      formData.append("photos", file);
    });

    const response = await axios.post("http://127.0.0.1:5000/api/todos", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    console.log(response.data);
    router.push("/");  // Перенаправление на главную страницу
  } catch (error) {
    console.error("Ошибка при добавлении задачи:", error);
  }
}

// Функция для вызова выбора файлов
function triggerFileInput() {
  const fileInput = document.getElementById("file-upload");
  fileInput.click();
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

/* Стили для предпросмотра изображений */
.image-previews {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.image-preview {
  position: relative;
}

.preview-image {
  max-width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 5px;
}

.remove-image-btn {
  position: absolute;
  top: -5px;
  right: -5px;
  background: rgba(255, 0, 0, 0.7);
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.remove-image-btn:hover {
  background: rgba(255, 0, 0, 1);
}

/* Модальное окно */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-image {
  max-width: 90%;
  max-height: 80%;
  object-fit: contain;
}

.custom-clear-icon {
  margin-left: 8px; /* Отступ от текста */
  vertical-align: middle; /* Вертикальное выравнивание по центру текста */
}
.animated-button {
  background-color: #72a2ac; /* Начальный цвет */
  color: white;
  transition: background-color 0.5s ease-in-out;
}

/* При наведении кнопка будет плавно менять цвета */
.animated-button:hover {
  animation: colorCycle 6s infinite; /* Плавная анимация перехода через цвета */
}

/* Анимация для плавного изменения цвета фона */
@keyframes colorCycle {
  0% {
    background-color: #72a2ac; /* #dae4e5 */
  }
  25% {
    background-color: #94c0c2; /* #94c0c2 */
  }
  50% {
    background-color: #69a4a2; /* #69a4a2 */
  }
  75% {
    background-color: #296e6b; /* #296e6b */
  }
  100% {
    background-color: #2b4a4a; /* #2b4a4a */
  }
}
</style>
