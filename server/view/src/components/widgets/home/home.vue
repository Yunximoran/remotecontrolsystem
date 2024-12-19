
<template>
    <div class="home">
        <div class="menu">
            <Settings></Settings>
            <Login></Login>
        </div>
        <!-- 基础控制按钮 -->
        <div class="container">
            <!-- 基本控制指令 -->
            <div class="core-left">
                <WaitDone>fesfe</WaitDone>
            </div>
            <div class="core-mid">
                <!-- 按键盒子 && 软件列表 -->
                <BtnBox @clicked="btnbox_event"></BtnBox>
                <Softwarebox></Softwarebox>
            </div>
              
            <!-- content -->
            <div class="core-right">
                <RouterView v-if="isshow_send"></RouterView>
                <ClientBox v-if="!isshow_send" @return="(val)=>{this.clients = val}"></ClientBox>
            </div>      
        </div>
        <div class="bottomBar">
            <Loger></Loger>
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
import Softwarebox from "./softwareview/softwarebox.vue";
import WaitDone from "./waitdone.vue"
import { useSocketStore } from "@/plugins/store/sockerStore";
import { useRootStore } from "@/plugins/store/rootStore";


export default{
    components: {
        Sendmodel,
        BtnBox,
        Settings,
        ClientBox,
        Login,
        Loger,
        Softwarebox,
        WaitDone
    },
    setup(){
        const sockerStore = useSocketStore()
        const rootStore = useRootStore()
        return {
            sockerStore,
            rootStore
        }
    },
    data(){
        return {
            selects: {},
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
        this.sockerStore.setupWebSocket()
        this.$router.afterEach((to, from) =>{
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
    align-items:flex-start;
    justify-items: center;   
}
.menu p, span{
    background-color: #798589;
    margin: 0;
}


/* CONTAINER */
.container{
    display: flex;
    align-self: flex-end;
    align-items: flex-end;
    flex-direction: row;
    height: 70vh;
    gap:10px;
}
.core-left{
    width: 22vw;
    display: flex;
    align-self: center;
    justify-self: center;
    height: 100%;
}
.core-mid{
    width: 42vw;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    align-self:flex-start;
    gap: 10px;

}

.core-right {
    margin-top: 12px;
    display: flex;
    margin-left: 10px;
    align-items: flex-start;
    width: 32vw;
    gap: 12px
}

.bottomBar{
    align-self: center;
    bottom: 10px;
    height: 20vh;
    width: 99%;
}
</style>
