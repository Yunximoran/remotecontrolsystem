import axios from 'axios'
import { createApp } from 'vue'


import App from './components/App.vue' // 导入组件
import router from "./components/router"
import store from './components/variable'


// content fastapi
axios.defaults.withCredentials = true
axios.defaults.baseURL = "http://127.0.0.1:8000" // 后端地址


const app = createApp(App)
app.use(router)
app.use(store)
app.mount("#app")

