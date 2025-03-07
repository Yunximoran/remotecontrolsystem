import {createRouter, createWebHistory} from "vue-router"

import User from "@/components/page/user.vue"
import Registry from "@/components/page/registry.vue"
import Login from "@/components/actions/submit_login_message.vue"
import Home from "@/components/widgets/home/home.vue"
import Sendmodel from "@/components/widgets/home/basecontrol/sendmodel.vue"
import DesposeInstruct from "@/components/actions/despose/despose_instruct.vue"
import DesposeSoftware from "@/components/actions/despose/despose_software.vue"

const routes = [
    {path: "/", redirect: "home"},
    {path: "/home", component: Home, children: [
        {path: "send", name: "sendmodel", component: Sendmodel},
    ]},
    {path: "/user/:uname?:account?", name: "user", component: User},
    {path: "/login", name: "login", component: Login},
    {path: "/registry", component: Registry},
    {path: "/despose", children:[
        {path: "instruct/:msg", component: DesposeInstruct},
        {path: "software/:msg", component: DesposeSoftware}
    ]}
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

export default router