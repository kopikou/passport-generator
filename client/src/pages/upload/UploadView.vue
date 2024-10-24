<script setup lang="ts">

import useUploadFileViewStore from "stores/uploadFileViewStore";
import {storeToRefs} from "pinia";

const uploadFileViewStore = useUploadFileViewStore();

const{
  admissionData,
}=storeToRefs(uploadFileViewStore)

</script>

<template>
  <div class="q-pa-lg">
    <div class="text-center text-h6 q-mb-md">Список рабочих программ ИРНИТУ</div>
    {{ admissionData }}
  </div>
</template>

<style scoped>

</style>
