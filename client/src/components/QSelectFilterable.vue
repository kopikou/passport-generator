<script setup lang="ts">
import {ref, useAttrs, watch} from 'vue'

const props = defineProps({
  options: {
    default: []
  },
  // modelValue: {
  //
  // }
})

const attrs = useAttrs()
const filteredOptions = ref();
// const emits = defineEmits(['@update:model-value'])

watch(() => props.options, () => {
  filteredOptions.value = props.options;
}, {
  immediate: true
})

function filterFn(val: any, update: any, abort: any) {
  update(() => {
    const needle = val.toLowerCase()
    filteredOptions.value = props.options.filter(v => v.toLowerCase().indexOf(needle) > -1)
  })
}
</script>

<template>
  <q-select v-bind="attrs" @filter="filterFn" :options="filteredOptions" />
</template>

<style scoped>

</style>
