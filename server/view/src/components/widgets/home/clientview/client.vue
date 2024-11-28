<template>
    <img class='client'
        ref = 'item'
        :ip="ip" 
        :src="require('@/assets/logo.png')"
        :alt="ip" 
        @click="selecting($event)"       
        @mouseenter="isfocus=true" 
        @mouseleave="isfocus=false">
</template>

<script>
import { ref, watch } from 'vue';
import { useRootStore } from '@/plugins/store/rootStore';

export default{
    props: ['ip', 'status'],

    setup(props){
        const rootStore = useRootStore()
        const isselect = ref()
        const isfocus = ref(false)
        const color = ref()

        function set_select_status(){
            return rootStore.selects[props.ip]
        }

        function  set_color(){
            return isselect.value ? "red" : (props.status === "true" ? "greenyellow" : "#bababa")
        }

        function selecting(event){
            rootStore.update_selected({
                0: props.ip,
                1: !isselect.value
            })
            isselect.value = set_select_status()
        }


        isselect.value = set_select_status()
        color.value = set_color()

        watch(isfocus, (nval)=>{
            if(!isselect.value){
                color.value = nval ? "red" : set_color()
            }
        })
        return {
            rootStore,
            isselect,
            isfocus,
            color,
            selecting,
        }
    },
    created(){
        console.log(this.rootStore.selects)
    }
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