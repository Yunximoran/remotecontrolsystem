
import {createStore} from "vuex"

const store = createStore({
    state(){
        return {
            softwares: []
        }
    },
    mutations:{
        add_software(state, item){
            console.log("add_software")
            console.log(state.softwares)
            state.softwares.push(item)
        }
    }
})

export default store