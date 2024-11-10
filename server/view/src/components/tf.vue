<template>
    <div @keydown="handleKeyDown" @keyup="handleKeyUp" tabindex="0">
        <h1>按下 Control + S 进行保存</h1>
    </div>
</template>

<script>
export default {
    data() {
        return {
            keysPressed: {}
        };
    },
    methods: {
        handleKeyDown(event) {
            // 记录按键状态
            this.keysPressed[event.key] = true;

            // 检测是否同时按下了 Control 和 S
            if (this.keysPressed['Control'] && this.keysPressed['s']) {
                event.preventDefault(); // 防止默认行为
                console.log('Control和S同时被按下！');
                // 触发相应操作，如保存
            }
        },
        handleKeyUp(event) {
            // 清除按键状态
            this.keysPressed[event.key] = false;
        }
    },
    mounted() {
        // 使 div 可聚焦以便接收键盘事件
        this.$el.focus();
    }
}
</script>

<style>
h1 {
    text-align: center;
    margin-top: 50px;
}
</style>
