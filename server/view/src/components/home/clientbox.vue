
<template>
    <div>
        <span v-if="clients" class="clients">
            <Client v-for="client in demo" :key="client" :ip="client.ip" :msg="client">logo</Client>

        </span>
    </div>
</template>

<script>
import axios from 'axios';
import Client from "./client.vue"

export default{
    data(){
        return {
            clients: [],
            demo: [1, 2, 3 ,4 ,5, 6, 7,8,9,10]
        }
    },
    components: {
        Client,   
    },

    methods: {
        getclientmessage(){
            axios.get("/servers/data/clientmessage/").then((res)=>{
                for (const client in res.data){
                   this.clients.push({...JSON.parse(res.data[client])}) 
                   console.log(this.clients)
                }
            })
        }
    },

    created(){
        // 这里是组件的钩子，组件被创建时调用
        this.getclientmessage()
    }
}
</script>

<style>
.clients {
    width: 30%;
    height: 80%;
    position: relative;
    top: 33px;
    display: grid;
    
    background-color: wheat;
    grid-template-columns: repeat(auto-fill, minmax(60px, 60px)); 
    gap: 3px;
}

</style>