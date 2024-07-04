<script setup lang="ts">

import useMainStore from "stores/mainStore";
import {storeToRefs} from "pinia";

const mainStore = useMainStore();

const {csrf} = storeToRefs(mainStore)

</script>

<template>
<div>
  <div class="q-pa-md">
    <q-uploader
      label="Auto Uploader"
      auto-upload
      url="/api/upload/insert_file/"
      multiple
      :headers="[{name: 'X-CSRFToken', value: csrf}]"
    />
  </div>
</div>
</template>

<style scoped>

</style>
