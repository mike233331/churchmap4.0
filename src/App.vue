<template>
  <div id="app">
    <!-- Логотип, который будет ссылаться на главную страницу -->
    <router-link to="/" className="logo-link">
      <img src="@/assets/churchphoto.png" alt="Logo" className="logo"/>
    </router-link>

    <!-- Основной контент приложения -->
    <div className="content">
      <!-- Рендеринг компонента HelloWorld для корневого маршрута -->
      <HelloWorld v-if="$route.path === '/'" msg="Welcome to Your Vue.js App"/>
      <AddChurch v-if="$route.path === '/addchurch'" msg="Welcome to Your Vue.js App"/>
      <!-- Рендеринг маршрутов для остальных страниц -->
      <router-view v-else/>
    </div>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue';
import AddChurch from "@/components/AddChurch.vue";

export default {
  name: 'App',
  components: {
    AddChurch,
    HelloWorld,
  },
};
</script>

<style>
body {
  background-image: url('/Users/misha/WebstormProjects/test_vue/my-project/src/assets/25547-zemlya-noch-prostranstvo-vselennaya-kosmos-1920x1080.jpg');
  background-repeat: no-repeat;
  background-size: cover;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

/* Стиль для логотипа */
.logo-link {
  position: absolute;
  top: 10px;
  left: 10px;
  display: inline-block;
  z-index: 10; /* Чтобы логотип был поверх других элементов */
}

.logo {
  width: 50px; /* Размер логотипа */
  height: auto;
}

/* Контейнер для основного контента */
.content {
  padding-top: 70px; /* Отступ сверху, чтобы контент не скрывался за логотипом */
}
</style>