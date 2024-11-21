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
                    <input type="text" placeholder="name"
                        v-model="software.ecdis.name" 
                        @keyup.enter="addsoftware(software)">
                </div>
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

<script>
import axios from 'axios';

export default{
    props: {
        clients: Object
    },
    data() {
        return{
            shells: [],
            shell: {
                name: null,
                shell: null
            },

            softwares: [],
            software:{
                ecdis: {
                    name: null,
                    version: "null"
                },
                conning: false
            }
        }
    },

    methods: {
        // add 
        addshell(shell){
            const s = shell.name || shell.shell
            const n = shell.name && shell.shell
            if(s){ // 至少有个为真
                if(!n){
                    if(s == shell.name){
                        this.$refs.ss.focus()
                    }
                    else{
                        this.$refs.sn.focus()
                    }
                }
                else{
                    this.shells.push(JSON.parse(JSON.stringify(shell)))
                    shell.name = null
                    shell.shell = null
                    this.$refs.sn.focus()
                }
            }
            else{
                if(!(this.shells.length === 0)){
                    this.sendshells()
                }
            }
        },

        addsoftware(software){
            const temp = software
            if (software.ecdis.name){
                this.softwares.push(JSON.parse(JSON.stringify(software)))
                software.ecdis.name = null
            }
            else{
                if(!(this.softwares.length === 0)){
                    this.sendsoftwares()
                }
            }
        },

        // clean
        clean(obj){
            obj.length = 0
        },

        // send
        sendshells(){
            const params = this.shells
            this.shells = []
            axios.put("/servers/send_control_shell", params).then((res) =>{
                console.log(res.data)
            })
        },
        sendsoftwares(){
            const params = this.softwares
            this.softwares = []
            axios.put("/servers/send_software_checklist/", params).then((res)=>{
                console.log(res.data)
            })
        }
    },
    
}
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