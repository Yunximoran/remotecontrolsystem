
<template>
   <!-- 需要输入框，输入shell后回车添加进 -->
    <form @keyup.enter.prevent="addshell(shell)">
        <input type="text" v-model="shell.name">
        <input type="text" v-model="shell.shell">
        <P>{{ shells }}</P>
    </form>


    <button @click.prevent="sendshell">send shell</button>

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
            var i = shell
            if(shell.name && shell.shell){
                this.shells.push({...shell})
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
