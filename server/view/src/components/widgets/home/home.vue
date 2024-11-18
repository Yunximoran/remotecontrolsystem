
<template>
    <div class="home">
        <div class="menu">
            <Settings></Settings>
            <Login></Login>
        </div>
        <!-- 基础控制按钮 -->
        <div class="container">
            <!-- 基本控制指令 -->
            <BtnBox @clicked="btnbox_event"></BtnBox>   
            <!-- content -->
            <div class="core">
                <RouterView v-if="isshow_send"></RouterView>
                <!-- <Sendmodel style="
                margin-right:80px;
                " v-if="isshow_send" :clist="clients">
                </Sendmodel> -->
                <Loger v-if="!isshow_send"></Loger>
                <ClientBox v-if="!isshow_send" @return="(val)=>{this.clients = val}"></ClientBox> <!--客户端预览 -->
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
import Loger from "./loger.vue";


export default{
    components: {
        Sendmodel,
        BtnBox,
        Settings,
        ClientBox,
        Login,
        Loger,
    },
    data(){
        return {
            clients: {},
            isshow_send: false,
        }
    },
    methods:{
        btnbox_event(label){
            switch(label){
                case "custom commands":{
                    this.isshow_send = !this.isshow_send
                    if(this.isshow_send){
                        this.$router.push({name: "sendmodel"})
                    }
                    else{
                        this.$router.push("/home")
                    }
                }
            }
            
        }
    },
    created(){
        this.$router.afterEach((to, from) =>{
            // console.log(to)
            // console.log(from)
            if(this.$route.path === "/home"){
                this.isshow_send = false
            }
        })
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
.container{
    display: flex;
    margin-left: auto;
    align-items: center;
    flex-direction: column;

}
.core {
    margin-top: 12px;
    display: flex;
    margin-left: 10px;
    align-items: flex-start;
    gap: 12px

}
</style>
