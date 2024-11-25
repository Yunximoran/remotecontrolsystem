
<template>
    <div v-if="clients" class="clients">
        <Client ref='item' v-for="(status, ip) in clients" :key="status" :ip="ip" :status="status"></Client>
    </div>
</template>

<script>
import axios from 'axios';
import Client from "./client.vue"


export default{
    data(){
        return {
            isclear: false,
        }
    },
    components: {
        Client,   
    },
    computed:{
        clients(){
            return this.$store.state.clients
        },
        selects(){
            return this.$store.state.selects
        }
    },
    watch: {

    },

    methods: {
        getclientmessage(){
            axios.get("/servers/data/client_status/")
            .then((res)=>{
                console.log(res.data)
                this.$store.commit("add_clients", res.data)
                return res.data
            }).then((data) =>{
                console.log("init selects")
                this.$store.commit("init_selects", data)
            }).catch((error)=>{
                console.log(error)
            })
        }, 
    },
    created(){
        // 这里是组件的钩子，组件被创建时调用
        this.getclientmessage()
        this.$emit("return", this.selects)
        
    },
}
</script>

<style>

.clients {
    position: relative;
    border: 3px solid red;
    width: 32vw;
    height:68vh;
    display: grid;
    background-color: wheat;
    grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));  
    grid-template-rows: repeat(auto-fill, minmax(60px, 1fr));
    border-radius: 10px;
    place-items: center;
    padding: 6px;
    overflow-y: scroll;
    gap: 3px;
}

.clients::-webkit-scrollbar{
    width: 10px;
}

.clients::-webkit-scrollbar-track{
    background-color: aqua;
}

.clients::-webkit-scrollbar-thumb{
    background-color: red;
}

</style>