<template>
    <div class="menu">
        <span ref="settings" class="settings" @click="loadoptions(this.$refs.settings, 'SETTINGS', options, 0)">
            <p>SETTINGS</p>
        </span>
        <span class="login">
            <p>LOGIN</p>
        </span>
    </div>
</template>

<script>
import axios from "axios";
import { createElementBlock } from "vue";
export default{
    data(){
        return {
            // 设置选项
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

            // 选项级别
            option_level: [
                'level_0',
                "level_1",
                "level_2",
                "level_3",
                "level_4",
                "level_5",
            ],

            // 选项标记： 是否展示子选项
            is_show_options: [
                false,
                false,
                false,
                false,
                false,
                false,
            ]
        }
    },
    methods: {
        set_conf(){
            axios.put('/settings/serverport').then((res)=>{
                this.setting = res.data
            })
        },

        loadoptions(node, label, options, level){
            this.is_show_options[level] = !this.is_show_options[level]
            if (this.is_show_options[level]) {
                this.addsettings(node, options, level)
            }
            else {
                this.removesettings(node, label)
            }

        },

        addsettings(parent, options, level){
            for (let option in options){
                let current = document.createElement('span')
                let title = document.createElement('p')

                title.textContent = option

                console.log(typeof level)
                current.className = this.option_level[level]
                current.appendChild(title)

                if (typeof options[option] === 'object'){
                    // 怎么设置同级别共用一个is_show
                    current.onclick = (event) => {
                        event.stopPropagation();
                        this.loadoptions(current, option, options[option], level+1)
                    }
                }
                else {
                    current.onclick = () => this.alter(option)
                }

                parent.appendChild(current)
            }
        },
        removesettings(element, label){
            element.innerHTML = `<p>${label}</p>`
        },
        alter(option){
            alert(`alter ${option} option`)
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
    user-select: none;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-items: center;
    height: 30px;
    
}
.menu p, span{
    background-color: #798589;
    margin: 0;
    /* margin: 0; */
}


/* settings  */
.menu span{
    width: 120px;
    height: 100%;
    margin: 0 10px 0 10px;
    color: #c02e2e;
    text-align: center;
    line-height: 30px;
    border-radius: 3px;

}
span.level_0{
    position: relative;
    margin: 0;
    color: gold
}
span.level_1{
    position: relative;
    bottom: 30px;
    left: 120px;
    margin: 0;
    color: rebeccapurple
}
span.level_2{
    position: relative;
    bottom: 30px;
    left: 120px;
    margin: 0;
    color: green
}
</style>