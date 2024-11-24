import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';  // Axios для HTTP-запросов

const app = createApp(App);

app.config.globalProperties.$axios = axios; // Сделаем axios доступным во всей программе

app.use(router).mount('#app');