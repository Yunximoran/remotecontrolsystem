<template>
    <div class="waitdone">
        <Tasklist/>
    </div>
</template>


<script setup>
import Tasklist from './tasklist.vue';

</script>

<style>
.waitdone{
    display: block;
    margin: 10;
    background-color: white;
    width: 100%;
    height: 100%;
    border-radius: 30px;
}
</style>