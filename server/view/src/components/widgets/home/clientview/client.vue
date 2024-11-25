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
export default{
    props: ['ip', 'status'],
    data(){
        return {
            isselect: false,    // 是否选中
            isfocus: false,     // 是否聚焦
            isclick: false,     // 是否点击
            color: this.set_color(),
         }
    },
    computed:{
        selects(){
            return this.$store.state.selects
        }
    },
    watch:{
        isfocus(nval){
            if (!this.isselect) {
                this.color = nval ? "red" : this.set_color()
            }
        },
        isselect(nval){
            this.color = nval ? "red" : this.set_color()
            this.$store.commit("update_selected", {
                0: this.$props.ip,
                1: nval
            })
        }
    },
    methods:{
        selecting(event){
            // event.ctrlKey
            this.isselect = !this.isselect
        },
        set_color(){
            return this.$props.status === "true" ? "greenyellow" : "#bababa"
        }
    },
    created(){
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