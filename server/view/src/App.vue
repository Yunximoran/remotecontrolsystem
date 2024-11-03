
<template>
   <!-- 控制台 -->
    <Settings style="
        margin-left:30px;
        margin-bottom:60px
        "
    ></Settings>
    <Sendmodel style="
        margin-left:80px;
        "
    ></Sendmodel>



</template>
<script>
import Sendmodel from "./components/sendmodel.vue";
import Settings from "./components/settings.vue";


export default{
  components: {
    Sendmodel,
    Settings,
  },
  render(){
    const inp = h('input', {
                class: 'alter',
                id: current.textContent,
                type: 'text',
                onKeyup: withModifiers((event) => {
                    axios.put('/servers/settings/alter/', {
                        option: option,
                        nval: event.target.value
                    })
                }, ['enter'])
            })
            // inp.render()
          return
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
