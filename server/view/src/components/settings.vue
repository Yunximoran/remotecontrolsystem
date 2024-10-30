<template>
    <div class="menu">
        <span 
            class="settings" @click="showsettings = true" @mouseleave="showsettings = false">

            <span>SETTINGS</span>
            
            <span
                v-if="showsettings"
                v-for="(value, key) in options" 
                @click="showoptions_level_1 = true" 
                @mouseleave="showoptions_level_1 = false">

                <p>{{ key }}
                    <ul v-if="showoptions_level_1" v-for="(o, n) in value"
                        @click="showoptions_level_2 = true" 
                        @mouseleave="showoptions_level_2 = false">
                        <p>{{ n }}
                            <ul v-if="showoptions_level_2" v-for="(so, sn) in o">
                                <p 
                                @click="showoptions_level_3=true"
                                @mouseleave="showoptions_level_3=false">
                                <p @click="isHovered=true">{{ sn }}</p>
                                </p>
                                <input v-if="(showoptions_level_3 && isHovered)" type="text" :placeholder="so">
                            </ul>
                        </p>

                    </ul>
                </p>
            </span>
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
    /* width: 30px; */
    height: 100%;
    margin: 0 10px 0 10px;
    /* background-color: #424242; */
    color: #bebebe;
    text-align: center;
    line-height: 30px;
    padding: 3px;
    border-radius: 3px;
}

.menu span span{
    margin: 0px;
    padding: 0px;
    color: white;
}

.menu p {
    background-color: greenyellow;
    font: 18px;
    margin: 0;
}

</style>