<template>
    <!-- 数据发送模块 -->
    <div class="sendbox">
        <div class="sends">
            <div class="send shell">
                <div class="inputshell">
                    <input ref="sn" type="text" placeholder="name"
                        v-model="shell.name"
                        @keyup.enter="addshell(shell)">
                        <br>
                    <input ref="ss" type="text" placeholder="shell"
                        v-model="shell.shell"
                        @keyup.enter="addshell(shell)">
                </div>
                <button @click="clean(shells)">clean</button>
                <button @click="sendshells">send</button>
            </div>
            <div class="send software">
                <div class="inputsoftware">
                    <!-- 
                        输入软件名称从中找到软件， 可以从路径中找到
                    -->
                    <input type="text" placeholder="name"
                        v-model="software.ecdis.name"
                        list="softwareview"
                        @keyup.enter="addsoftware(software)">
                </div>
                <select id="softwareview" v-if="searchview.length !== 0"
                    @click="select_software($event)"
                    style="
                        position: absolute;
                        width: 100px;
                    "
                    :size="searchview.length"
                >
                        <option v-for="item of searchview" :value="item">{{ item }}</option>
                </select>
                <button @click="clean(softwares)">clean</button>
                <button @click="sendsoftwares">send</button>
            </div>

        
        </div>
        <div class="sendview">
            <span class="show">
                SHELL LIST
                <p v-for="(s, i) in shells">
                    ITEM:  {{ i }}
                    <br>
                    {{ s }}
                </p>
            </span>
            <span class="show">
                SOFTWARE LIST
                <p v-for="(s, i) in softwares">
                    ITEM: {{ i }} <br>
                    {{ s }}
                </p>
            </span>
        </div>  
    </div>
</template>

<script setup>
import axios from 'axios';
import { useRootStore } from '@/plugins/store/rootStore';
import { useSocketStore } from '@/plugins/store/sockerStore';
import { ref, watch} from 'vue';
import { useTemplateRef } from 'vue';
import { version } from 'core-js';

const rootStore = useRootStore()
const socketStore = useSocketStore()
const props = defineProps({
    clients: Object
})

const ss = useTemplateRef("ss")
const sn = useTemplateRef("sn")
const shells = ref([])
const shell = ref({
    name: null,
    shell: null
})

const softwares = ref([])
const searchview = ref([])
const software = ref({
        ecdis: {
            name: null,
            version: "null"
        },
        conning: false
    })

function addshell(shell){
    // const ss = useTemplateRef("ss")
    // const sn = useTemplateRef("sn")
    const s = shell.name || shell.shell
    const n = shell.name && shell.shell
    if(s){ // 至少有个为真
        if(!n){
            if(s == shell.name){
                ss.value.focus()
            }
            else{
                sn.value.focus()
            }
        }
        else{
            shells.value.push(JSON.parse(JSON.stringify(shell)))
            shell.name = null
            shell.shell = null
            sn.value.focus()
        }
    }
    else{
        if(!(shells.value.length === 0)){
            sendshells()
        }
    }
}
function addsoftware(software){
    // 只能添加软件清单存在的内容
    if(!(softwares.value.length === 0)){
        sendsoftwares()
    }
    if (searchview.value.length !== 0){
        for (const item of searchview.value){
            const sp = item.split(/[\\/]/)

            softwares.value.push({
                ecdis: {
                    name: sp[sp.length-1],
                    version: "null"
                },
                conning: false
            })
        }
    }
    else{
        console.log("软件不存在")
    }
    software.ecdis.name = null

}

function clean(obj){
    obj.length = 0
}

function sendshells(){
    const params = {
        shell_list: shells.value,
        toclients: rootStore.selecteds
    }
    shells.value = []
    console.log("shells params", params)
    axios.put("/servers/send_control_shell/", params)
    .then((res) =>{
        console.log("sent to clients", rootStore.selecteds)
    }).catch(error=>{
        console.log(error)
    })
}

function sendsoftwares(){
    const params = softwares.value
    softwares.value = []
    axios.put("/servers/send_software_checklist/", params).then((res)=>{
        console.log(res.data)
    })
}

function select_software(event){
    const sp = event.target.value.split(/[\\/]/)
    const select = sp[sp.length-1]
    software.value.ecdis.name = select
    event.target.blur()
}
watch(()=> software.value.ecdis.name, (nval, oval)=>{
    searchview.value = []
    if (nval !== ''){
        const pattern = new RegExp(nval, "i")
        console.log(socketStore.data.softwarelist)
        for (const item of socketStore.data.softwarelist){
            // D://geek.exe
            // item.substring(0, item.lastIndexOf("."))

            if(item.substring(0, item.lastIndexOf(".")).match(pattern)){
                const sppath = item.split(/[\\/]/)
                const softname = sppath[sppath.length-1]
                searchview.value.push(item)
            }
        }         
    }
    console.log("searchview", searchview.value)

})
/*
// export default{

//     // props: {
//     //     clients: Object
//     // },
//     // data() {
//     //     return{
//     //         shells: [],
//     //         shell: {
//     //             name: null,
//     //             shell: null
//     //         },

//     //         softwares: [],
//     //         software:{
//     //             ecdis: {
//     //                 name: null,
//     //                 version: "null"
//     //             },
//     //             conning: false
//     //         }
//     //     }
//     // },
//     computed:{
//         // ...mapStores(useRootStore),
//         ...mapState(useRootStore, ['selecteds'])
//     },
//     methods: {
//         // add 
//         addshell(shell){
//             const s = shell.name || shell.shell
//             const n = shell.name && shell.shell
//             if(s){ // 至少有个为真
//                 if(!n){
//                     if(s == shell.name){
//                         this.$refs.ss.focus()
//                     }
//                     else{
//                         this.$refs.sn.focus()
//                     }
//                 }
//                 else{
//                     this.shells.push(JSON.parse(JSON.stringify(shell)))
//                     shell.name = null
//                     shell.shell = null
//                     this.$refs.sn.focus()
//                 }
//             }
//             else{
//                 if(!(this.shells.length === 0)){
//                     this.sendshells()
//                 }
//             }
//         },

//         addsoftware(software){
//             const temp = software
//             if (software.ecdis.name){
//                 this.softwares.push(JSON.parse(JSON.stringify(software)))
//                 software.ecdis.name = null
//             }
//             else{
//                 if(!(this.softwares.length === 0)){
//                     this.sendsoftwares()
//                 }
//             }
//         },

//         // clean
//         clean(obj){
//             obj.length = 0
//         },

//         // send
//         sendshells(){
//             const params = {
//                 shell_list: this.shells,
//                 toclients: this.selecteds
//             }
//             this.shells = []
//             console.log("shells params", params)
//             axios.put("/servers/send_control_shell/", params)
//             .then((res) =>{
//                 console.log("sent to clients", this.selecteds)
//             }).catch(error=>{
//                 console.log(error)
//             })
//         },

//         sendsoftwares(){
//             const params = this.softwares
//             this.softwares = []
//             axios.put("/servers/send_software_checklist/", params).then((res)=>{
//                 console.log(res.data)
//             })
//         }
//     },
    
// }
*/
</script>


<style>
.sendbox {
    display: flex; 
    width: 100%;
    height: 100%;
    flex-direction: column; 
    align-items: center;
    align-self: center;
    justify-self: center;
}

.sends{
    display: flex;
    align-items: start;
    justify-items: space-around;
    margin-bottom: 100px;
}
.send {
    float: left;
    margin: 10px 76px 10px 76px;

}

.sendview{
    float: right;
    display: flex;
    align-items: flex-start;
}

.send input {
    height: 18px;
    width: 120px;
    line-height: 18px;
    border: #9ea4e6 ridge 3px;
    border-radius: 5px;
}

.send.software input{
    height: 42px;
}


/* ====== span style ====== */
span.show {
    display: inline-block;
    width: 300px;
    height: 320px;
    overflow-y:auto;
    /* line-height: 15px; */
    background-color: #fabfab;
    border: 1px solid #ccc;
    border-radius: 3px;
    text-align: center;
    word-wrap: break-word;
}

/* span scrollbar */
span.show::-webkit-scrollbar{
    width: 10px;
}
span.show::-webkit-scrollbar-track{
    background-color: #9ea4e6;
    border-radius: 2px;
}
span.show::-webkit-scrollbar-thumb{
    background-color: aqua;
    border-radius: 5px;
}

/* span p */
span.show p{
    margin: 3px;
}
</style>