<template>
    <img class='client'
        ref = 'item'
        :ip="ip" 
        :src="config.logo"
        :alt="ip" 
        @click="selecting()"       
        @mouseenter="start=true" 
        @mouseleave="start=false">
</template>

<script>
import { mapGetters } from 'vuex';
export default{
    props: ['ip', 'status'],
    data(){
        return {
            isselect: false,
            start: false,
            defalut_color: "#bababa",
            color: null,
            status: this.$props.status,
            isclick: false,
         }
    },
    computed:{
        ...mapGetters({
            config: "getconfig_client"
        })
    },
    watch: {
        start: {
            handler(nval, oval){
                if(this.isclick === false){
                    if(nval){
                        this.color = 'red'
                    }
                    else{
                        this.color = this.defalut_color
                    }
                }
            }
        },
        status(nval){
            if (nval === "true"){
                this.defalut_color = "greenyellow"
            }
            else{
                this.defalut_color = "#bababa"
            }
        },
    },

    methods:{
        selecting(){
            this.isclick = !this.isclick
            if(this.isclick){
                this.color = "red"
            }
        },
    },
    created(){
        if (this.status === "true"){
            this.defalut_color = "greenyellow"
        }
        this.color = this.defalut_color
        console.log(this.status)
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