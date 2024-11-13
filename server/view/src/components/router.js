import {createRouter, createWebHistory} from "vue-router"

import App from "./App.vue"
import User from "./page/user.vue"

const routes = [
    {path: "/user", component: User}
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

export default router