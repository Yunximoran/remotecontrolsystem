<template>
    <!-- 通过代开资源管理器添加软件 -->
     <div class="softwarebox">
        <tabel>
            <tr>
                <th>软件名称</th>
                <th>连接状态</th>
            </tr>
            <tr v-for="software in rootStore.softwares" :key="software">
                <td>{{software.ecdis.name}}</td>
                <td>{{ software.conning }}</td>
            </tr>
        </tabel>
     </div>
</template>


<script>
import axios from 'axios';
import { useRootStore } from '@/plugins/store/rootStore';
import { mapStores } from 'pinia';

// 软件列表保存本地
export default{
    data(){
        return {
            
        }
    },
    computed:{
        ...mapStores(useRootStore)
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