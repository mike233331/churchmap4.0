<template>
  <div id="app">
    <!-- Рендеринг компонента HelloWorld для корневого маршрута -->
    <HelloWorld v-if="$route.path === '/'" msg="Welcome to Your Vue.js App" />

    <!-- Рендеринг маршрутов для остальных страниц -->
    <router-view v-else />
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue';

export default {
  name: 'App',
  components: {
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
</style>
