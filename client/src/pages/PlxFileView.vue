<script setup lang="ts">

import axios from "axios";
import {onBeforeMount} from "vue";

const props = defineProps( {
    id: {
    required: true,
    type: Number
  }
})

async function getFileData() {
  console.log(props.id)
  let r = await axios.get("api/upload/get_file_by_id/", {params: {id: props.id} })
  console.log(r.data.items)
}

onBeforeMount(() => {
  getFileData()
})

</script>

<template>
<div>
  hello world!
</div>
</template>

<style scoped>

</style>
