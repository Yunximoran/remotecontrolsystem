<template>
    <!-- 通过代开资源管理器添加软件 -->
     <div class="softwarebox">
        {{ $store.state.softwares }}
     </div>
</template>


<script>
import axios from 'axios';

export default{
    data(){
        return {
            
        }
    },
    methods:{
        get_softwarelist(){
            axios.get("/servers/data/softwarelist")
            .then((res)=>{

            })
            .catch((error)=>{
                console.log(error)
            })
        },
    },
    created(){
        this.get_softwarelist()
    },
}
</script>

<style>
.softwarebox{
    width: 98%;
    height: 90%;
    border-radius: 15px;
    background-color: white;
    z-index: 2;
    /* margin-top:10px; */
}

/* .softwarebox table{

}

.softwarebox button{
    
} */
</style>