<template>
    <div>USERNAME: {{ $route.params.uname }}</div>

    <li v-for="item in account" :key="item">
        {{ item }}
    </li>
</template>

<script>
import axios from 'axios';

export default{
    data(){
        return {
            account: null,
        }
    },
    methods:{
        get_user_information(){
            axios.get("/servers/data/accounts", {
                params: {
                    account: this.$route.params.account
                }
            })
            .then((res)=>{
                this.account = res.data
                console.log(res.data)
            })
            .catch((error)=>{
                console.log(error)
            })
        }
    },
    mounted(){
        this.get_user_information()
    }
}

</script>