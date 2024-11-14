<template>
    <form ref="submit">
        <input ref="username" type="text" @keyup.enter="inp_username_event" v-model="username">
        <input ref="password" tpye="password" @keyup.enter="inp_password_event($event)" v-model="password">

        <p>{{ username }}</p>
        <p>{{ password }}</p>
        <button @click.prevent="$router.push('/registry')">注册</button>
        <button @click.prevent="submitlogin">登录</button>
    </form>
</template>

<script>
import axios from 'axios';
import { nextTick } from 'vue';

export default{
    data(){
        return {
            username: null,
            password: null
        }
    },
    methods:{
        submitlogin(){
            axios.post("/servers/login/", {
                "username":this.username,
                "password":this.password
            }).then((res)=>{
                
                this.$router.push({
                    name: "user",
                    params: {
                        uname: this.username
                    }
                })
            }).catch((error)=>{
                console.log(error)
            })
        },
        inp_username_event(){
            nextTick(()=>{
                this.$refs.password.focus()
            })
        },
        inp_password_event(event){
            if(this.username && this.password){
                this.submitlogin()
            }
        },
    }
}
</script>
