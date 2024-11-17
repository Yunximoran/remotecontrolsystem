
<template>
    <div class="home">
        <div class="menu">
            <Settings></Settings>
            <Login></Login>
        </div>
        <!-- 基础控制按钮 -->
        <div class="container">
            <!-- 基本控制指令 -->
            <BtnBox></BtnBox>   
            <!-- content -->
            <div class="core">
                <Sendmodel style="
                margin-right:80px;
                "></Sendmodel>          <!--自定义指令 -->
                <ClientBox></ClientBox> <!--客户端预览 -->
            </div>            
        </div>
    </div>
</template>


<script>
import Sendmodel from "./basecontrol/sendmodel.vue";
import Settings from "../menu/settings.vue";
import Login from "../menu/login.vue";
import BtnBox from "./basecontrol/btnbox.vue"
import ClientBox from "./clientview/clientbox.vue"


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


/* HOME */
.home{
    display: flex;
    flex-direction: column;
    gap: 10px;
}


/* MENU */
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


/* CONTAINER */
.core {
    display: flex;
    float: right;
    margin-left: 10px;
    justify-items: flex-end;
}
</style>
