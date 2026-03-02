import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const htmlElement = document.documentElement;
const savedTheme = localStorage.getItem("color-theme");

if (
  savedTheme === "dark" ||
  (!savedTheme &&
    window.matchMedia("(prefers-color-scheme: dark)").matches)
) {
  htmlElement.classList.add("dark");
} else {
  htmlElement.classList.remove("dark");
}

createApp(App)
  .use(router)
  .mount('#app')