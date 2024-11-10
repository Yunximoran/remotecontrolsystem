
import App from './App.vue' // 导入组件
import axios from 'axios'

axios.defaults.withCredentials = true
axios.defaults.baseURL = "http://127.0.0.1:8000" // 后端地址

// import { createApp } from 'vue'
// const app = createApp(App)
// app.mount("#app")

import Vue from "vue"
import VueRouter from "vue-router"

Vue.useAttrs(VueRouter)

const router = new VueRouter({
    routes: [
        {
            path: '/',
            name: "Home",
            component: App
        }
    ]
})


router.beforeEach((to, from, next) => {
    next("/")
})

export default router

