<template>
    <!-- 数据发送模块 -->
    <div class="sendbox">
        <div class="sends">
            <div class="send shell">
                <div class="inputshell">
                    <input type="text" placeholder="name"
                        v-model="shell.name"
                        @keyup.enter="addshell(shell)">
                        <br>
                    <input type="text" placeholder="shell"
                        v-model="shell.shell"
                        @keyup.enter="addshell(shell)">
                </div>
                <button @click="clean(shells)">clean</button>
                <button @click="sendshells">send</button>
            </div>

            <div class="send software">
                <div class="inputsoftware">
                    <input type="text" placeholder="name"
                        v-model="software.name" 
                        @keyup.enter="addsoftware(software)">
                </div>
                <button @click="clean(softwares)">clean</button>
                <button @click="sendsoftwares">send</button>
            </div>
        </div>

        <div class="output">
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
    data() {
        return{
            shells: [],
            shell: {
                name: null,
                shell: null
            },

            softwares: [],
            software:{
                name: null,
                start: false
            }
        }
    },

    methods: {
        // add 
        addshell(shell){
            if (shell.name && shell.shell){
                this.shells.push({...shell})
                shell.name = null
                shell.shell = null
            }
        },
        addsoftware(software){
            if (software.name){
                this.softwares.push({...software})
                software.name = null
            }
        },

        // clean
        clean(obj){
            obj.length = 0
        },

        // send
        sendshells(){
            axios.put("/servers/send_control_shell", this.shells).then((res) =>{
                this.shells = []
            })
        },
        sendsoftwares(){
            axios.put("/servers/send_software_checklist/", this.softwares).then((res)=>{
                this.softwares = []
            })
        }
    },
    
}
</script>


<style>
.sendbox {
    float:left;
    display: flex; 
    flex-direction: column; 
    align-items: center;
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

.output{
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