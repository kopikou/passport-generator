<script setup lang="ts">

import useMainStore from "stores/mainStore";
import {storeToRefs} from "pinia";
import {useQuasar} from "quasar";

const mainStore = useMainStore();
const {csrf} = storeToRefs(mainStore)

const $q = useQuasar()

function filefilter(files) {
  return files.filter(file => file.name.slice(file.name.lastIndexOf(".")) == ".plx")
}

function onRejected(rejectedEntries) {
  $q.notify({
    type: 'negative',
    message: `${rejectedEntries.length} файл не прошли проверку, загружайте только файла расширения .plx`,
  })
}

</script>

<template>
<div>
  <div class="q-pa-md row justify-center">
    <q-uploader
      class="text-center"
      label="Загрузка файлов"
      bordered
      flat
        color="amber"
        text-color="black"
      auto-upload
      url="/api/upload/insert_file/"
      multiple
      accept=".plx"
      :filter="filefilter"
      :headers="[{name: 'X-CSRFToken', value: csrf}]"
      @rejected="onRejected"
    />
  </div>
</div>
</template>

<style scoped>

</style>
