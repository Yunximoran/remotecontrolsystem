<template>
    <div class="menu">
        <span class="settings">
            <p>SETTINGS</p>
        </span>
        <span class="login"><p>LOGIN</p></span>
    </div>
</template>
<script>
import axios from "axios";

export default{
    data(){
        return {
            options:{
                port:{
                    udp:{
                        server: 8081,
                        borad: 8082,
                        multi: 8083,
                        client: 8084,
                    },
                    tcp: {
                        server: 9095,
                        client: 8085
                    }
                }
            },
            setting: false,
        }
    },
    methods: {
        set_conf(){
            axios.put('/settings/serverport').then((res)=>{
                this.setting = res.data
            })
        }
    }
}
</script>

<style>
.menu{
    display: flex;
    flex-direction: row;
    height: 30px;

}

.menu span{
    height: 100%;
    margin: 0 10px 0 10px;
    background-color: #424242;
    color: #bebebe;
    text-align: center;
    line-height: 30px;
    padding: 3px;
    border-radius: 3px;
}

.menu p {
    font: 18px;
    margin: 0;
}

</style>