import { createRouter, createWebHistory } from 'vue-router';
import TodoView from './components/TodoView.vue'; // Убедитесь, что путь правильный
import AddChurch from "@/components/AddChurch.vue";
import EditTodo from './components/EditTodo.vue'


const routes = [
    {
        path: '/changes/:id',  // Параметр :id для задания ID задачи
        name: 'EditTodo',
        component: EditTodo
    },
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
