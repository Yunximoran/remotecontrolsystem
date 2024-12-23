
<template>
    <div v-if="socketStore.data.client_status" class="clients">
        <Client ref='item' v-for="(status, ip) in socketStore.data.client_status" :key="status" :ip="ip" :status="status"></Client>
    </div>
</template>

<script>
import axios from 'axios';
import Client from "./client.vue"
import { useRootStore } from "@/plugins/store/rootStore"
import { useSocketStore } from '@/plugins/store/sockerStore';
import { ref } from 'vue';

export default{
    setup(){
        const rootStore = useRootStore()
        const socketStore = useSocketStore()
        return {
            rootStore,
            socketStore 
        }
    },
    data(){
        return {
            isclear: false,
        }
    },
    components: {
        Client,   
    },

    watch: {

    },

    methods: {
    },
    created(){
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