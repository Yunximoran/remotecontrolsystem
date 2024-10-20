
<template>

<button @click="getMessage">第一个按钮</button>
<p>{{ msg }}</p>


<button @click="sendshell">shell msg: {{ shell }}</button>
</template>

<script>
import axios from 'axios';

export default{
  data(){
    return {
      msg: "Hello World",
      shell: null
    }
  },

  methods: {  
      getMessage() {
        axios.get("/testapi/").then((res) => {
          this.msg = res.data
        })
    }, 
    sendshell(){
      axios.put("/servers/send_control_shell", [
        {
          name: "first",
          shell: "Hello server"
        }
      ]).then((res) => {
        this.shell = res.data
      })
    }
    
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
</style>
