
import { createStore } from "vuex"

export const vuex_client = {
    state(){
        return {
            DEFAULTCOLOR: "#bababa",
            LOGO: require("@/assets/logo.png"),
        }
    },
    getters:{
        getconfig_client: (state)=>{
            return {
                defalut_color: state.DEFAULTCOLOR,
                logo: state.LOGO
            }
        },
    },
    multation:{
        set_default_color(state, Status){
            state.DEFAULTCOLOR = Status === "true" ? "greenyellow" : "#bababa"
        },
        setLogo(state, path){
            state.LOGO = require(path)
        }
    }
}
