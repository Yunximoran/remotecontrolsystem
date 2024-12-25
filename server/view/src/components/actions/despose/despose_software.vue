<template>
    <div class="despose">
        <div class="software">
            <li v-for="item in donedata.data" :key="item" @click="select_software_path(item)">{{ item }}</li>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useSocketStore } from '@/plugins/store/sockerStore';
import { onMounted } from 'vue';

const route = useRoute()
const router = useRouter()
const socketStore = useSocketStore()

const donedata = ref(JSON.parse(route.params.msg))
function select_software_path(choosed){
    axios.put("/servers/despose/waitdone/",{
            "msg": route.params.msg,
            "results": choosed
        }).then(res=>{
        console.log(res)
    }).catch(err=>{
        console.log(err)
        console.log(choosed)
    }).finally(()=>{
        router.push("/home")
    })
}

onMounted(()=>{
    console.log("mounted")
})


</script>