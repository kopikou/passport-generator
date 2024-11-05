<script setup lang="ts">


import { ref, watch } from "vue";
import {api} from "boot/axios";

const props = defineProps({
  title: {
    required: true
  },
  fileId: {
    required: true
  }
})

const file = ref()

watch(file, async () => {
  const formData = new FormData()
  formData.append('file', file.value)
  formData.append('type', 'document')
  let r = await api.post(`/api/upload/${props.fileId}/save-file/`, formData)
})

</script>

<template>
  <q-file
      :label="props.title"
      v-model="file"
      outlined
      stack-label
      dense
      style="width: 100%;"
      @update:modelValue="console.log(file)"
  >
  </q-file>
</template>

<style scoped>

</style>
