<script setup lang="ts">

const props = defineProps({
  data: {
    require: true,
  }
})

</script>

<template>
<div>
  {{ props.data }}
</div>
</template>

<style scoped>

</style>
