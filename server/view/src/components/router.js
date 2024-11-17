import {createRouter, createWebHistory} from "vue-router"

import App from "./App.vue"
import User from "./page/user.vue"
import Login from "./actions/submit_login_message.vue"
import Home from "./widgets/home/home.vue"
import Registry from "./page/registry.vue"

const routes = [
    {path: "/", redirect: "home"},
    {path: "/home", component: Home},
    {path: "/user/:uname?:account?", name: "user", component: User},
    {path: "/login", name: "login", component: Login},
    {path: "/registry", component: Registry}
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

export default router