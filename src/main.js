import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';  // Axios для HTTP-запросов
import { Quasar } from 'quasar';
import 'quasar/dist/quasar.css'



const app = createApp(App);


app.use(Quasar, {
    config: {
        brand: {
            primary: '#027be3',
            secondary: '#26a69a',
            accent: '#9c27b0'
        },
    }
})

app.config.globalProperties.$axios = axios; // Сделаем axios доступным во всей программе

app.use(router).mount('#app');