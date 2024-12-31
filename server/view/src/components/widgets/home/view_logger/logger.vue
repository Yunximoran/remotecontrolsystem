<template>
    <div class="output">
        <li v-for="log in socketStore.data.logs" :key="report">{{ JSON.parse(log).data }}</li>
    </div>
</template>



<script setup>
import { useSocketStore } from '@/plugins/store/sockerStore';
const socketStore = useSocketStore()

// var



// function

// watch

// computed

// hook



</script>
<style>
.output{
    display: inline-block;
    background-color: white;
    width: 100%;
    height: 100%;
    border-radius: 15px;
}
/* .output::-webkit-scrollbar{

}
.output::-webkit-scrollbar-track{

}
.output::-webkit-scrollbar-thumb{

} */
</style>
