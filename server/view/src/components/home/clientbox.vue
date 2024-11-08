
<template>
    <div v-if="clients" class="clients">
            <Client ref='item' @click="selectclient([client, i])" v-for="(client, i) in demo" :key="client" :ip="client.ip" :msg="client"></Client>
    </div>
</template>

<script>
import axios from 'axios';
import Client from "./client.vue"

export default{
    data(){
        return {
            clients: [],
            demo: [1, 2, 3 ,4 ,5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,32, 33, 34, 35,36],
            select: [],
        }
    },
    components: {
        Client,   
    },
    watch: {
        select: {
            handler(nval, oval){
                console.log(this.select)
            }
        }
    },

    methods: {
        getclientmessage(){
            axios.get("/servers/data/clientmessage/").then((res)=>{
                for (const client in res.data){
                   this.clients.push({...JSON.parse(res.data[client])}) 
                   console.log(this.clients)
                }
            })
        },

        selectclient(item){
            let is_exist = false
            if(this.select.length === 0) {

            }
            else{            
                for(const c of this.select){
                    if (c[1] === item[1]){
                        is_exist = true
                        break
                    }
                }
            }
            if (!is_exist) {
                this.select.push([...item])
                console.log([...item])
                console.log(this.select)
                console.log("ok, selected a item")
            }
            else{
                console.log("the item is exist")
            }
        },

    },


    created(){
        // 这里是组件的钩子，组件被创建时调用
        this.getclientmessage()
        document.addEventListener("click", (event)=>{

        })
    },

}
</script>

<style>

.clients {
    position: relative;
    border: 3px solid red;
    width: 32vw;
    height:80vh;
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