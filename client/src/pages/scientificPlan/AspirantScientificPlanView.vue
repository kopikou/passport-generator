<script setup lang="ts">

const props = defineProps({
  id: {
    required: true,
    type: Number,
  }
})

</script>

<template>
<div class="q-pa-lg">
  {{ props.id }}
</div>
</template>

<style scoped>

</style>
