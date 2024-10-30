
<template>
   <!-- 控制台 -->
    <Settings style="
        margin-left:30px;
        margin-bottom:60px
        "
    />
    <Sendmodel style="
        margin-left:80px;
        "
    />
    




</template>
<script setup>
import Sendmodel from "./components/sendmodel.vue";
import Settings from "./components/settings.vue"
</script>



<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 30px;
}

/* global */
body {
    background-color: #a29bc2;
    /* position: relative; */
}

button {
  background-color: rgb(175, 220, 171);
  color:rgb(21, 73, 55);
  border-radius: 3px;
}


</style>
