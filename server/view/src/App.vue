
<template>
   <!-- 需要输入框，输入shell后回车添加进 -->
    <form @submit.prevent="addshell">
        <input type="text" v-model="shell.name">
        <input type="text" v-model="shell.shell">
    </form>
    <button @click="sendshell"></button>

</template>

<script>
import axios from 'axios';
export default{
    data(){
        return {
            msg: null,
            shells: [],
            shell: {
                name: null,
                shell: null,
            },
    }
  },

    methods: { 

        addshell(shell){
            if(this.shell.name && this.shell.shell){
                this.shells.push(this.shell)
                this.shell.name = null
                this.shell.shell = null
            }
        },

        getMessage() {
            axios.get("/testapi/").then((res) => {
            this.msg = res.data
            })
        }, 

        sendshell(){
            axios.put("/servers/send_control_shell", this.shells).then((res) => {
                    this.shell = res.data
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

button {
  background-color: rgb(0, 84, 108);
  color:aquamarine;
}

</style>
