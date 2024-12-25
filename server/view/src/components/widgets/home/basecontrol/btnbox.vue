<template>
    <div class="btnbox">
        <button v-for="(action, btn) in btns" :key='btn' class="btn" :name="btn" :ref="btn" @click="action">{{btn}}</button>
    </div>
</template>

<script>
import axios from 'axios';
import { mapStores } from 'pinia';
import { useRootStore } from '@/plugins/store/rootStore';
import { useSocketStore } from '@/plugins/store/sockerStore';

export default{
    setup(){
        const socketStore = useSocketStore()
        return {
            socketStore
        }
    },
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
                    // alert("add new software")
                    axios.put("/servers/data/alter", null,{
                        params: {
                            alter: "push"
                        }
                    })
                    .then((res)=>{
                        console.log(res.data)

                        // 新加入的软件默认为未连接状态
                        const software = {
                            "ecdis":{
                                "name": res.data.OK,
                                "version": "1.0.1"
                            },
                            "conning": false
                        }
                        // 服务端可能不需要也安装软件
                        this.rootStore.add_software(software)
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
                    axios.put("/servers/send_control_shell/", {
                        shell_list: [{
                            name: 'close -s',
                            shell: null
                        }],
                        tocliencts: this.rootStore.selected()
                    })
                    alert("close all software")
                },

                openAllSoftWare: ()=>{
                    this.$emit("clicked")
                    alert("open all software")
                },

                downloadFile: ()=>{
                    axios.post("/servers/data/alter", null, {
                        params: {
                            alter: "download"
                        }
                    }).then(res=>{
                        console.log("downloaing")
                    }).catch(err=>{
                        console.log("error downloaded")
                    })
                },

                batchOperation: ()=>{
                    this.$emit("clicked")
                    alert("batch operation")
                },

                customCommands: ()=>{
                    this.$emit("clicked", "custom commands")
                }
            } 
        }
    },
    computed:{
        ...mapStores(useRootStore)
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