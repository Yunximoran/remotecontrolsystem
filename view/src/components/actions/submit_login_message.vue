<template>
    <form ref="submit">
        <input ref="account" type="text" @keyup.enter="inp_account_event($event)" v-model="account">
        <input ref="password" tpye="password" @keyup.enter="inp_password_event($event)" v-model="password">
    </form>
    <button @click.prevent="$router.push('/registry')">注册</button>
    <button @click.prevent="submitlogin">登录</button>
</template>

<script>
import axios from 'axios';
import { nextTick } from 'vue';

export default{
    data(){
        return {
            account: null,
            password: null
        }
    },
    methods:{
        submitlogin(){
            axios.post("/servers/login/", {
                "account":this.account,
                "password":this.password
            }).then((res)=>{
                const usermsg = res.data.msg
                this.$router.push({
                    name: "user",
                    params: {
                        uname: usermsg.username,
                        account: usermsg.account
                    }
                })
            }).catch((error)=>{
                console.log(error)
            })
        },
        inp_account_event(event){
            nextTick(()=>{
                this.$refs.password.focus()
            })
        },
        inp_password_event(event){
            if(this.account && this.password){
                this.submitlogin()
            }
        },
    }
}
</script>
