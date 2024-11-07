<template>
    <img class='client'
        ref = 'item'
        :ip="ip" 
        :src="require('@/assets/logo.png')"
        :alt="ip" 
        @mouseenter="start=true" 
        @mouseleave="start=false">
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
    },
}
</script>
<style>
.client {
    overflow: hidden;
    width: 60px;
    height: 60px;
    background-color: v-bind(color);
    border-radius: 5px;
    margin: 3px;
    padding: 1px;
}

</style>