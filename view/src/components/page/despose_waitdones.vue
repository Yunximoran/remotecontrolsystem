<template>
    <div class="despose">
        <div v-if="donetype"></div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';


const route = useRoute()

const msg = JSON.parse(route.params.msg)
const donetype = ref(msg.type)
const donedata = ref(msg.data)

</script>