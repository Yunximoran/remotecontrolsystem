<template>
    <div class="despose">
        <div class="instruct">
            <SendModel/>
            <form>
                <input/>
                <input/>
            </form>
            <button @click="clear">clear</button>
            <button @click="send">send</button>
            <span class="view">{{ donedata }}</span>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute()
const router = useRouter()

const donedata = ref(JSON.parse(route.params.msg))
const shells = ref([])
const shell = ref({
    name: null,
    shell: null
})

function addshells(){

}

function clear(){

}

function send(){
    axios.put("/servers/event/desposed_waitdones/", {
        data: {
            msg: JSON.stringify({
                type: 'instruct',
                data: donedata
            }),
            results: item
        }
    }).then(res=>{
        console.log(res)
    }).catch(err=>{
        console.log(err)
    }).finally(()=>{
        // 返回主页
        router.push("/")    
    })
}
</script>