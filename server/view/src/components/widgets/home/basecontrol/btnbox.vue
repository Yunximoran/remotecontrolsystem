<template>
    <div class="btnbox">
        <button v-for="(action, btn) in btns" :key='btn' class="btn" :name="btn" :ref="btn" @click="action">{{btn}}</button>
    </div>
</template>

<script>
import axios from 'axios';
import { render, h } from 'vue';
export default{
    data(){
        return {
            btns: { // name: [show, action]
                closeClients: () =>{
                    alert("close all clients")
                },
                openClients: ()=>{
                    alert("open all Clients")
                },
                restartClients: ()=>{
                    alert("restart all clients")
                },
                addSoftware: ()=>{
                    alert("add new software")
                    axios.put("/servers/data/alter", null,{
                        params: {
                            alter: "push"
                        }
                    }
                    )
                    .then((res)=>{

                    })
                    .catch((error)=>{
                        console.log(error)
                    })
                },
                openSoftware: ()=>{
                    this.$emit("clicked")
                    alert("open the software")
                },
                closeAllSoftWare: ()=>{
                    this.$emit("clicked")
                    alert("close all software")
                },
                openAllSoftWare: ()=>{
                    this.$emit("clicked")
                    alert("open all software")
                },
                downloadFile: ()=>{
                    this.$emit("clicked")
                    alert("download file")
                },
                batchOperation: ()=>{
                    this.$emit("clicked")
                    alert("batch operation")
                },
                customCommands: ()=>{
                    this.$emit("clicked", "custom commands")
                    alert("customCommands")
                }
            } 
        }
    },
    watch:{

    },
    methods:{

    }
}
</script>

<style>
.btnbox{
    /* position:absolute */
    display: flex;
    width: 100%;
    height: 10%;
    flex-wrap: wrap;
    flex-direction: row;
    justify-content: space-between;
    gap: 6px;
    z-index: 1;
}

.btnbox button{
    width:calc((100% / 5) - 6px);
    height: 30px;
    line-height: 30px;
    overflow: hidden;
    text-align: center;
    padding: 0;
    /* margin: 0 6px 0 6px; */
    /* margin: 0; */
}
</style>