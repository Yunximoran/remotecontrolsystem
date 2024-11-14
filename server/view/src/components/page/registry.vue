<template>
    <form class="registry">
        <ul v-for="(_, fn) in formlist">{{ fn }}: <input v-model="formlist[fn]"></ul>
        <button @click.prevent="submit_registry">submit</button>
    </form>

    <p v-for="item in formlist">{{item}}</p>
</template>

<script>
import axios from 'axios';

export default{
    data(){
        return {
            formlist: {
                username: null,
                password: null,
                repassword: null,
            },
        }
    },
    methods:{
        submit_registry(){
            try{
                axios.put("/servers/data/registry_account", this.check_message())
                .then((res)=>{
                    console.log("success registry a account", res.data.username)
                    console.log(res.data)
                })
                .catch((error)=>{
                    console.log(error)
                })
                .finally(()=>{
                    for(const item in this.formlist){
                        this.formlist[item] = null
                    }
                })
            }
            catch(error){
                console.log(error)
            }
        },

        check_message(){
            const data = {}
            for(const item in this.formlist){
                // console.log(item)
                if (this.formlist[item] === null) {
                    throw new Error("null")
                }
                else{
                    data[item] = this.formlist[item]
                }
            }
            // console.log(data)
            return data
        }
    }
}
</script>