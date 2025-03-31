<!-- eslint-disable vue/multi-word-component-names -->
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
        const rootStore = useRootStore()
        return {
            socketStore,
            rootStore
        }
    },
    data(){
        return {
            btns: { // name: [show, action]
                closeClients: () =>{
                    axios.post("/servers/sends/instruct", {
                        shell_list: [{
                            name: 'close',
                            shell: ""
                        }],
                        tocliencts: this.rootStore.selecteds
                    }).then(res=>{
                        console.log(res)
                    }).catch(err=>{
                        console.log(err)
                    })
                },

                openClients: ()=>{
                    axios.put("/servers/event/wol", {
                        tocliencts: this.rootStore.selecteds
                    }).then(res=>{
                        console.log(res)
                    }).catch(err=>{
                        console.log(err)
                    })
                },

                restartClients: ()=>{
                    axios.post("/servers/sends/instruct", {
                        shell_list: [{
                            name: 'restart',
                            shell: ""
                        }],
                        tocliencts: this.rootStore.selecteds
                    }).then(res=>{
                        console.log(res)
                    }).catch(err=>{
                        console.log(err)
                    })
                    alert("close all software")
                },

                addSoftware: ()=>{
                    // alert("add new software")
                    const sf = {
                        ecdis: {
                            name: "geek",
                            path: "D://geek"
                        },
                        conning: false
                    }
                    axios.put("/server/event/addsoftwarelist", sf)
                    // .then((res)=>{
                    //     console.log(res.data)

                    //     // 新加入的软件默认为未连接状态
                    //     const software = {
                    //         "ecdis":{
                    //             "name": res.data.OK,
                    //             "path": null
                    //         },
                    //         "conning": null
                    //     }
                    //     this.rootStore.add_software(software)
                    // })
                    .catch((error)=>{
                        console.log(error)
                    })
                },

                openSoftware: ()=>{
                    this.$emit("clicked")
                    axios.post("/servers/sends/instruct", {
                        shell_list:[{
                            name: "start -s",
                            shell: this.rootStore.selecteds_software
                        }]
                    }).then(res=>{
                        console.log(res)
                    }).catch(err=>{
                        console.log(err)
                    })

                },

                closeAllSoftWare: ()=>{
                    axios.post("/servers/sends/instruct", {
                        shell_list: [{
                            name: 'close -s',
                            shell: "all"
                        }],
                        tocliencts: this.rootStore.selecteds
                    }).then(res=>{
                        console.log(res)
                    }).catch(err=>{
                        console.log(err)
                    })
                },

                openAllSoftWare: ()=>{
                    axios.post("/servers/sends/instruct", {
                        shell_list: [{
                            name: 'start -s',
                            shell: "all"
                        }],
                        tocliencts: this.rootStore.selecteds
                    }).then(res=>{
                        console.log(res)
                    }).catch(err=>{
                        console.log(err)
                    })
                },

                downloadFile: ()=>{
                    axios.put("/servers/event/download", {
                        tocliencts: this.rootStore.selecteds
                    }).then((res)=>{
                        console.log("downloaing", res)
                    }).catch((err)=>{
                        console.log("error downloaded", err)
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