<script setup lang="ts">


import {ref, watch} from "vue";
import {api} from "boot/axios";
import _ from "lodash";
import useUploadFileViewStore from "stores/uploadFileViewStore";
import {storeToRefs} from "pinia";
import {useQuasar} from "quasar";


const uploadFileViewStore = useUploadFileViewStore();

const {
  admissionData
} = storeToRefs(uploadFileViewStore)

const props = defineProps({
  title: {
    required: true,
  },
  fileId: {
    required: true,
  },
  planId: {
    required: true,
  }
})
const $q = useQuasar()
const file = ref()

function fileFilter(files) {
  return files.filter(file => file.type === 'application/pdf')
}

watch(file, async () => {
  $q.loading.show()
  const formData = new FormData()
  formData.append('file', file.value)
  formData.append('type', 'document')
  formData.append('fileId', props.fileId)
  let r = await api.post(`/api/upload/${props.planId}/save-file/`, formData)

  let admKey = _.findKey(admissionData.value, (x) => x.plan_id == props.planId)
  admissionData.value[admKey].documents_files.push(r.data)

  $q.loading.hide()
})

</script>

<template>
  <q-file
      :label="props.title"
      v-model="file"
      outlined
      stack-label
      dense
      accept=".pdf"
      :filter="fileFilter"
      @rejected="$q.notify({type: 'info', message: 'Можно загрузить только файлы формата pdf'})"
      style="width: 100%;"
  >
  </q-file>
</template>

<style scoped>

</style>
