import { createApp } from 'vue'
import App from './App.vue' // 导入组件
import axios from 'axios'

axios.defaults.withCredentials = true
axios.defaults.baseURL = "http://127.0.0.1:8000" // 后端地址


/*
menu

console

nav

login server
    * manage admin user
    * user message 
    * 
show client message
    * choose client list
alter server config


send software check list
send control shell
    common instructons
*/
const app = createApp(App)
app.mount("#app")



