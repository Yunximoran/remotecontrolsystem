
<template>

<button @click="getMessage">{{ msg }}</button>
</template>

<script>
import axios from 'axios';

export default{
  data(){
    return {
      msg: "Hello World"
    }
  },

  methods: {  
      getMessage() {
        axios.post("/send").then((res) => {
          this.msg = res.data;        
        });
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
</style>
