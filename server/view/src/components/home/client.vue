<template>
    <span class="client" :ip="ip">
        <!-- logo or item -->
        <img :src="require('@/assets/logo.png')" :alt="ip" @mouseenter="start=true" @mouseleave="start=false">
    </span>
</template>

<script>
import axios from 'axios';

export default{
    props: ['ip', 'msg'],
    data(){
        return {
            start: false,
            color: '#bababa'
         }
    },

    watch: {
        start: {
            handler(nval, oval){
                if(nval){
                    this.color = 'red'
                }
                else{
                    this.color = '#bababa'
                }
            }
        }
    }
}
</script>
<style>
.client {
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    width: 60px;
    height: 60px;
    background-color: v-bind(color);
    border-radius: 5px;
    margin: 3px;
    padding: 1px;
}
.client img{
    height: 100%;
    width: 100%;
    margin: 3px;
}
</style>