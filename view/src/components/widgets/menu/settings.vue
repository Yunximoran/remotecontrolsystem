<template>
    <span ref="settings" class="settings" @click="loadoptions(this.$refs.settings, 'SETTINGS', options, 0)">
            <p>SETTINGS</p>
    </span>
</template>

<script>
import axios from "axios";
import { h, render } from "vue";


export default{
    data(){
        return {
            // 设置选项
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
                        client: 8085,
                    }
                },
                demo: 'null',
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
            ],
        }
    },
    methods: {

        loadoptions(node, label, options, level){
            console.log(node.querySelectorAll('span').length)
            const is_unfold = node.querySelectorAll('span').length === 0 // 判断该选项是否展开

            if (is_unfold){
                this.is_show_options[level] = false
            }
            else{
                this.is_show_options[level] = true
            }

            this.is_show_options[level] = !this.is_show_options[level]

            if (this.is_show_options[level]) {
                this.addsettings(node, options, level)
            }
            else {
                this.removesettings(node, label)
            }

        },

        addsettings(parent, options, level){
            // create a set of options on the parent element
            for (let option in options){
                let current = document.createElement('span')
                let title = document.createElement('p')

                title.textContent = option

                current.className = this.option_level[level]
                current.appendChild(title)
                if (typeof options[option] === 'object'){
                    // 设置同级别共用一个is_show
                    // 是否有其他同级别节点
                    current.onclick = (event) => {
                        event.stopPropagation()
                        this.checkcolleagues(parent, option)
                        this.loadoptions(current, option, options[option], level+1)
                    }
                }
                else {
                    current.onclick = (event) => {
                        event.stopPropagation()
                        this.checkcolleagues(parent, option)
                        this.alter(current, option, options[option])
                    }
                }

                parent.appendChild(current)
            }
        },

        removesettings(element, label){
            // reinitialize the element named label
            element.innerHTML = `<p>${label}</p>`
        },

        checkcolleagues(parent, selfname){ 
            // check if other colleagues are saved
            const colleagues = parent.querySelectorAll('span')
            for (const colleague of colleagues){
                
                const is_unfold = colleague.querySelectorAll('span').length !== 0
                const label = colleague.querySelector('p').textContent

                if (is_unfold && selfname != label){
                    this.removesettings(colleague, label)
                }
            }
        },


        alter(current, option, value){
            // create alter entry
            const inp = h('input', {
                    class: 'alter',
                    id: option,
                    type: 'text',
                    placeholder: value,
                    onkeyup:(event) => {
                        event.stopPropagation()
                        if (event.key === 'Enter'){
                            console.log(event.target.value)
                            axios.put("/servers/alter/settings/port/", null, {
                                    params:{
                                        option: option,
                                        nval: event.target.value
                                    }
                                }).then(res => {
                                    console.log(res.data)
                                }).catch(error => {
                                    console.log(error.message)
                                }).finally(() => {
                                    event.target.blur()
                                })
                        }
                    },

                    onblur: (event) => {
                        console.log("input event")
                        try{
                            render(null, current)
                        }catch(error){
                            console.log(error)
                        }
                    },

                    onclick: (event) =>{
                        event.stopPropagation()
                        
                    },
                })
            
            // whether other input tags exist 
            const otherAlters = this.$refs.settings.querySelectorAll('.alter')
            if (otherAlters.length === 0){
                render(inp, current) // rendering to current node
            }
            else {
                render(null, current) // remoded from the current node
            }

            // the input is automatically focused rendered
            this.$nextTick(() => {
                const inputElement = current.querySelector(`#${option}`)
                if (inputElement){
                    inputElement.focus()
                }
            })
        },

        
    },
}


</script>

<style>


/* settings  */
.menu span{
    width: 120px;
    height: 100%;
    margin: 0 10px 0 10px;
    color: #c02e2e;
    text-align: center;
    line-height: 30px;
    border-radius: 3px;
    display: flex;
    flex-direction: column;
}

.settings span p{
    border-radius: 3px;
}

span.level_0{
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    margin: 0;
    color: gold
}

span.level_1{
    width: 60px;
    display: flex;
    flex-direction: column;
    position: relative;
    bottom: 30px;
    left: 90px;
    margin: 0;
    color: rebeccapurple
}
span.level_2{
    width: 60px;
    display: flex;
    flex-direction: column;
    position: relative;
    bottom: 30px;
    left: 60px;
    margin: 0;
    color: green
}

.alter{
    position:relative;
    width: 60px;
    top: -100%;
    left: 100%;
    border: red 2px;
    /* border-radius: 15px; */
}
</style>