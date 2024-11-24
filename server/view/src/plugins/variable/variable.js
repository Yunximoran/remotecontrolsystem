
import {createStore} from "vuex"

import {vuex_client} from "./config/client"

export const store = createStore({
    state(){
        return {
            softwares: [],
            clients: {},
            demo: []
        }
    },
    getters:{
        getDemo: (state)=>{state.demo}
    },
    mutations:{
        add_software(state, item){
            console.log("add_software")
            console.log(state.softwares)
            state.softwares.push(item)
        },
        add_clients(state, data){
            state.clients = data
        }
    },
    modules:{
        config_client: vuex_client
    }
})
