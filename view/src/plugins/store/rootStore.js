
import { defineStore } from "pinia"

export const useRootStore = defineStore("root", {
    state: ()=>({
            selects: {},
            softwares: [],
            selects_software: {}
        }),
    getters:{
        selecteds: (state) => {
            //  确保发送时client处于正在链接
            const selected = []
            for (const key in state.selects){
                if(state.selects[key]){
                    selected.push(key)
                }
            }
            console.log("selected ", selected)
            return selected
        },
        seletceds_software: (state) =>{
            const selected = state
            return selected
        }
    },
    actions:{
        add_software(item){
            console.log("add_software")
            console.log(this.softwares)
            this.softwares.push(item)
        },
        pop_software(item){
            console.log("pop_software")
            this.softwares.pop(item)
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