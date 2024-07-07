<script setup lang="ts">

const props = defineProps({
  id: {
    require: true,
    type: Number,
  }
})

</script>

<template>
<div>
  hello world! discipline view {{ props.id }}
</div>
</template>

<style scoped>

</style>
