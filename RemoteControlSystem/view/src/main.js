import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'

axios.defaults.withCredentials = true
axios.defaults.baseURL = "http://127.0.0.1:8000" // 后端地址

const app = createApp(App)
app.mount("#app")



