<template>
    <span :ip="ip" style="
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        width: 60px;
        height: 60px;
        background-color: aqua;
        border-radius: 5px;
        margin: 3px;
    ">
        <!-- logo or item -->
        <img :src="require('@/assets/logo.png')" :alt="ip" style="
            width: 80%;
            height: 80%;
        ">
    </span>
</template>

<script>
import axios from 'axios';

export default{
    props: ['ip', 'msg'],

    data(){
        ids: []
    },
    method:{
        checkclientconnect(){
            axios.get("/servers/data/client/connect", {
                params: {
                    ip: this.ip
                }
            })
        },

        setupSSE(){
            new EventSource('/servers/checkout/connect')
            this.eventSource.onmessage = (event) => {
                const newData = JSON.parse(event.data)

            }
        }
    }
}
</script>

<style>

</style>