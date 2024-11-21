<template>
    <!-- 通过代开资源管理器添加软件 -->
     <div class="softwarebox">
        <table>
            <tr>
                <th>名称</th>
                <th>软件状态</th>
            </tr>
            <tr v-for="software in softwarelist" :key="software">
                <td>{{software.name}}</td>
                <td>{{software.start}}</td>
            </tr>
        </table>
        <ul v-for="software in softwarelist" :key="software">
            
        </ul>
        <button @click="get_softwarelist">刷新</button>
     </div>
</template>


<script>
import axios from 'axios';

export default{
    data(){
        return {
            softwarelist: []
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
        // 每次执行修改后重新获取数据
        add_software(item){
            axios.put("/servers/alter/data", item)
            .then((res)=>{
                this.get_softwarelist()
            })
            .catch((error)=>{
                console.log(error)
            })
        },
        /* 
        item: {
            alter,  put or delete
            object, software
        }
        */
        pop_software(item){
            axios.delete("/servers/alter/data", item)
            .then((res)=>{
                this.get_softwarelist()
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