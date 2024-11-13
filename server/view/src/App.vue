
<template>
   <!-- menu  -->
    <div class="menu">
        <Settings></Settings>
        <Login></Login>
    </div>
    <!-- 基础控制按钮 -->
     <div class=btnbox>
        <BtnBox></BtnBox>
     </div>
    <!-- content -->
    <div class="core">
        <Sendmodel style="
        margin-right:80px;
        "
        ></Sendmodel>
        <ClientBox></ClientBox>
    </div>
</template>


<script>
import Sendmodel from "./components/home/basecontrol/sendmodel.vue";
import Settings from "./components/menu/settings.vue";
import Login from "./components/menu/login.vue";
import BtnBox from "./components/home/basecontrol/btnbox.vue"
import ClientBox from "./components/home/clientview/clientbox.vue"


export default{
    components: {
        Sendmodel,
        BtnBox,
        Settings,
        ClientBox,
        Login,
    },
    data(){
        return {
            clients: {}
        }
    },
    created(){
        
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

.menu{
    /* position:relative; */
    user-select: none;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-items: center;
    height: 30px;
    
}
.menu p, span{
    background-color: #798589;
    margin: 0;
}

.core {
    display: flex;
    float: right;
    margin-left: 10px;
    justify-items: flex-end;
}


</style>
