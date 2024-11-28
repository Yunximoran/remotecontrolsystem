
import {createStore} from "vuex"

import {vuex_client} from "./config/client"

export const store = createStore({
    state(){
        return {
            softwares: [],
            clients: {},
            selects: {},
            demo: [],
        }
    },
    getters:{
        getDemo: (state)=>{state.demo},
        selecteds(state){
            const selected = []
            for (const key in state.selects){
                if (state.selects[key]){
                    selected.push(key)  // 返回携带客户端ip地址的列表
                } 
            }
            // console.log("getter selecteds")
            return selected
        }
    },
    mutations:{
        add_software(state, item){
            console.log("add_software")
            console.log(state.softwares)
            state.softwares.push(item)
        },

        add_clients(state, data){
            state.clients = data
        },

        init_selects(state, data){
            for (const key in data){
                state.selects[key] = false
            }
        },

        update_selected(state, param){
            state.selects[param[0]] = param[1]
            console.log(state.selects)
        },
    },
    modules:{
        config_client: vuex_client
    }
})
