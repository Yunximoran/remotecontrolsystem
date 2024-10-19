import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'

axios.defaults.withCredentials = true
axios.defaults.baseURL = "https://localhost:8000" // 后端地址

const app = createApp(App)
app.mount("#app")



