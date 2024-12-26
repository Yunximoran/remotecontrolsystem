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
const cookie = donedata.value.cookie
function select_software_path(choosed){
    console.log("msg", route.params.msg)
    console.log("choosed", choosed)
    axios.put("/servers/despose/waitdone/", {
        cookie: cookie,
        results: choosed
    }).then(res=>{
        console.log("choosed ok:", choosed)
        console.log(res)
    }).catch(err=>{
        // console.log("send error", choosed)
        console.log("type cookie", cookie)
        console.log(choosed)
        console.log(err)
    }).finally(()=>{
        router.push("/home")
    })
}

onMounted(()=>{
    console.log("mounted")
})


</script>