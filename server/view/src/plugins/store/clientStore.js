import { defineStore } from "pinia";

export const useClientStore = defineStore("clientStore", {
    state: () => ({
        DEFAULTCOLOR: "#bababa",
        LOGO: require("@/assets/logo.png")
    }),
    getters:{
        getconfig_client: (state)=>{
            return {
                default_color: state.DEFAULTCOLOR,
                logo: state.LOGO
            }
        }
    },
    actions:{
        set_defalut_color(Status){
            this.DEFAULTCOLOR = Status === "true" ? "greenyellow": "#bababa"
        },
        setLogo(path){
            this.LOGO = require("path")
        }
    }
})