import {createRouter, createWebHashHistory} from "vue-router"
import UserView from "./components/menu/login.vue"

const routes = [
    {path: "/login", component: UserView}
]

const router = createRouter({
    history: createWebHashHistory(),
    routes: routes
})

export default router