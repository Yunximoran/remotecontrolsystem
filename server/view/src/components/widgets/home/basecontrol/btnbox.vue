<template>
    <div class="btnbox">
        <button v-for="(action, btn) in btns" :key='btn' class="btn" :name="btn">{{action}}</button>
    </div>
</template>

<script>
export default{
    data(){
        return {
            btns: { // name: [show, action]
                1: "rm",
                2: "cd",
                3: "ls",
                4: "sudo"
            } 
        }
    },
    watch:{

    },
    methods:{

    }
}
</script>