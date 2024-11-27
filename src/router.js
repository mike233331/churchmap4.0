import { createRouter, createWebHistory } from 'vue-router';
import TodoView from './components/TodoView.vue'; // Убедитесь, что путь правильный
import AddChurch from "@/components/AddChurch.vue";

const routes = [
    {
        path: '/todo/:id',
        name: 'TodoView',
        component: TodoView,
    },
    {
        path: '/addchurch',
        name: 'AddChurch',
        component: AddChurch
    }
    // Другие маршруты, если они есть
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
