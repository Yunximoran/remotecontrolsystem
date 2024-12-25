<template>
    <div>
        <button v-for="(status, msg) in socketStore.data.client_waitdone" :key="msg" @click="dps_waitdone(msg)">{{ msg }}</button>
    </div>
</template>

<script setup>
import { useSocketStore } from '@/plugins/store/sockerStore';
import { useRouter } from 'vue-router';
import { ref, computed, watch, onMounted} from 'vue';  // vue基础
import { render, h } from 'vue';    // 虚拟节点相关
import axios from 'axios';

const socketStore = useSocketStore()
const router = useRouter()

function dps_waitdone(msg) {
    /*
        点击进入处理页面
        处理选项
            选择软件地址
            发送自定义shell指令：
                执行指令时错误： 
                    可能的问题
                    * 输入错误
                    * 权限问题
                    * 依赖未启动
    */
    // 怎么在跳转路由是携带参数
    const topath = {...JSON.parse(msg)}.type
    console.log("topatp", topath)
    router.push({path:"/despose/" + topath + "/"+ msg})
}

function dps_return(response){
    axios.put("/servers/depsoes", {
        data: response
    }).then(res=>{
        console.log(res)
    }).catch(err=>{
        console.log(err)
    })
}

onMounted(()=>{
    console.log(socketStore.data.client_waitdone)
})

</script>

<style>

</style>