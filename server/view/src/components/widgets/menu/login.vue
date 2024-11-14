<template>
    <span ref="login" class="login" @click.prevent="formshow">
        <p>LOGIN</p>
    </span>
</template>

<script>
import {render, h, nextTick} from "vue"
import axios from "axios"

export default{
    data(){
        return{
            usernane: null,
            password: null,
            isshow: false,
        }
    },
    watch(){

    },
    mounted(){
        // document.addEventListener


    },
    methods:{
        formshow(){
            this.$router.push("/login")
        }
    },

}
</script>