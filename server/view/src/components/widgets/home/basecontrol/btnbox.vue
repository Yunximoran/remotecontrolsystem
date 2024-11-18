<template>
    <div class="btnbox">
        <button v-for="(action, btn) in btns" :key='btn' class="btn" :name="btn" @click="action">{{btn}}</button>
    </div>
</template>

<script>
import axios from 'axios';
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
    display: flex;
    width: 50vw;
    flex-wrap: wrap;
    flex-direction: row;
    gap: 10px;
}

.btnbox button{
    width: 8vw;
    height: 30px;
}
</style>