<template>
    <img class='client'
        ref = 'item'
        :ip="ip" 
        :src="require('@/assets/logo.png')"
        :alt="ip" 
        @click="selecting()"       
        @mouseenter="start=true" 
        @mouseleave="start=false">
</template>

<script>
export default{
    props: ['ip', 'msg'],
    data(){
        return {
            start: false,
            color: '#bababa',
            isclick: false,
         }
    },

    watch: {
        start: {
            handler(nval, oval){
                if(this.isclick === false){
                    if(nval){
                        this.color = 'red'
                    }
                    else{
                        this.color = '#bababa'
                    }
                }
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