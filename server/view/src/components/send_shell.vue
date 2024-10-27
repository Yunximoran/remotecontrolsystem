<template>
    <form>
        <input type="text" v-model="shellitem">
        <button @click="addshell">add shell</button>
        <p>{{  }}</p>
    </form>
</template>

<script>
    data() {
        return {
            shellitem: {
                name: null,
                shell: null
            },
            shells: []
        }
    }

    methods(){
        addshell(shellitem){
            shells.put(shellitem)
        }
    }
</script>