
import { defineStore } from "pinia"
import { useClientStore } from "./clientStore"


export const useRootStore = defineStore("root", {
    state: ()=>({
            clients: {},
            selects: {},
            softwares: [],
        }),
    getters:{
        selecteds: (state) => {
            const selected = []
            for (const key in state.selects){
                if(state.selects[key]){
                    selected.push(key)
                }
            }
            console.log("selected ", selected)
            return selected
        },
        all_store: (state) =>{
            const clientStore = useClientStore()
            return {
                ...clientStore
            }
        }
    },
    actions:{
        add_software(item){
            console.log("add_software")
            console.log(this.softwares)
            this.softwares.push(item)
        },

        add_clients(data){
            this.clients = data
        },

        init_selects(data){
            for (const key in data){
                this.selects[key] = false
            }
        },

        update_selected(param) {
            this.selects[param[0]] = param[1]
            console.log(this.selects)
        },
    }
    })