
<template>
   <!-- 需要输入框，输入shell后回车添加进 -->
    <dev class="main">
        <dev class="send select">
            <dev class="shellbox">
                <form class="shell_form" @keyup.enter.prevent="addshell(shell)">
                    <input class="shell_input" type="text" v-model="shell.name">
                    <br>
                    <input class="shell_input" type="text" v-model="shell.shell">
                    <P>{{ shells }}</P>
                </form>
                <button @click.prevent="clear(shells)">clear</button>
                <button @click.prevent="sendshell">send shell</button>
            </dev>

            <dev class="softwarebox">
                <form class="softwareform" @submit.prevent="addsoftware(software)">
                    <input class="softwareinput" type="text" v-model="software.name">
                    <p>{{ softwares }}</p>
                </form>
                <button @click="clear(softwares)">clear</button>
                <button @click.prevent="sendsoftware">send software</button>
            </dev>
        </dev>

        <dev class="output">
            <span>
                {{ shells }}
            </span>
            <span>
                {{ softwares }}
            </span>
        </dev>
    </dev>





</template>

<script>
import axios from 'axios';
export default{
    data(){
        return {
            shells: [],
            shell: {
                name: null,
                shell: null,
            },

            softwares: [],
            software: {
                name: null
            }
    }
  },

    methods: { 

        addshell(shell){
            console.log(this.shells)
            if(shell.name && shell.shell){
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

        clear(obj){
            obj.length = 0
        },

        sendshell(){
            axios.put("/servers/send_control_shell", this.shells).then((res) => {
                    this.shells = []
                })
        },

        sendsoftware(){
            axios.put("/servers/send_software_checklist/", this.softwares).then((res)=>{
                this.softwares = []
            })
        },
  }
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

/* global */
body {
    background-color: #a29bc2;
    /* position: relative; */
}

.main {
    display: flex;
    flex-direction: column;
    gap:10px;
}

button {
  background-color: rgb(175, 220, 171);
  color:rgb(21, 73, 55);
  border-radius: 3px;
}


/* set shell form */

.shellbox {
    float:left;
    margin: top 5px;
}
.shellbox button {
    float: left;
    width: 50%;
    /* margin-left:30px; */
}
.shell_form {
    width: 200px;
    height: 100px;
    padding-top: 16%;
    background-color: #5f8ab5;
    border: #2c3e50 solid 3px;
    border-radius: 10px;
    float: top;
}
.shell_input {
    border-radius: 5px;
}


/* send software */
.softwarebox {
    float:left;
    margin: top 5px;
}
.softwarebox button {
    float: left;
    width: 50%;
}
.softwareform {
    width: 200px;
    height: 100px;
    padding-top: 16%;
    background-color: #5f8ab5;
    border: #2c3e50 solid 3px;
    border-radius: 10px;
    float: top;
}
.softwareinput {
    border-radius: 5px;
}


/* set output */
.output {
    display: flex;
    flex-direction: row;
    
    width: 100%;
    height: 100%;
    background-color: green;
    position: relative;
    margin-right: 30px;
}

.output span{
    width: 100px;
    height: 100px;
    background-color: yellow;
    margin: 10px;
    /* float: left; */
    width: 40px;
    height: 80px;
}

.output p{
    color: red;
}
</style>
