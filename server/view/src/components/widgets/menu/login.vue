<template>
    <span ref="login" @click="user_message">
        LOGIN
    </span>
</template>

<script>
import {render, h} from "vue"
import axios from "axios"

export default{
    date(){
        return{
            usernane: null,
            password: null,
        }
    },
    watch(){

    },
    methods:{
        user_message(){
            const input_username = h('input', {
                type: 'text',
                placeholder: 'username',
                onkeyup: (event)=>{
                    event.stopPropagation()
                    if (event.key === "Enter"){
                        this.username = event.target.value
                    }
                }
            })

            const input_password = h('input', {
                type: 'password',
                placeholder: 'password',
                onkeyup: (event)=>{
                    event.stopPropagation()
                    if(event.key === "Enter"){
                        this.password = event.target.value
                        if(this.password !== null){
                            if(this.username !== null){
                                event.target.parentElement.click((event)=> {
                                    console.log(this.username)
                                    console.log(this.password)
                                })
                            }
                        }
                    }
                }   
            })

            const login_form = h('form', {
                onSubmit: (event)=>{
                    event.preventDefault()
                    axios.post("/servers/login/", {
                        username: this.username,
                        password: this.password
                    }).then((res)=>{
                        console.log(res)
                    }).catch((error)=>{
                        console.log(error)
                    })
                }
            }, [input_username, input_password])
            render(login_form, this.$refs.login)
        },
        inpevent(event, action){
            event.stopPropagation()
            if(event.key === "Enter"){
                action()
            }
        },
    },
}
</script>