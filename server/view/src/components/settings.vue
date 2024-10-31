<template>
    <div class="menu">
        <span class="settings" @click="load_settings(document.querySelector('.settings'), options)">
            <p>SETTINGS</p>
        </span>
        <span class="login">
            <p>LOGIN</p>
        </span>
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
                        server: this.setdemo,
                        borad: this.setdemo,
                        multi: this.setdemo,
                        client: this.setdemo,
                    },
                    tcp: {
                        server: this.setdemo,
                        client: this.setdemo
                    }
                },
                demo: this.setdemo
            },
            showsettings: false,
            showoptions_level_1: false,
            showoptions_level_2: false,
            showoptions_level_3: false,

            isHovered: false,
        }
    },
    methods: {
        set_conf(){
            axios.put('/settings/serverport').then((res)=>{
                this.setting = res.data
            })
        },
        alter(){
            this.isHovered = !this.isHovered
            this.showoptions_level_3 = !this.showoptions_level_3
        },

        load_settings(parent, options){
            for (option in options){
                current = document.createElement('span')

                title = document.createElement('p')
                title.textConntext = option
                
                current.appendChild(title)

                if (typeof value == Object){
                    this.load_settings(current, options[option])
                }
                else {
                    current.onClick(options[option])
                }

                parent.appendChild(current)
            }
        },

        setdemo(){
            console.log("demo settings")
            alert("demo func")
        }
    }
}
</script>

<style>
.menu{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-items: center;
    height: 30px;
}

.menu span{
    width: 120px;
    height: 100%;
    margin: 0 10px 0 10px;
    color: #c02e2e;
    text-align: center;
    line-height: 30px;
    padding: 3px;
    border-radius: 3px;
}
</style>