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
  },
  url: {
    type: String
  },
  maxFileSize: {
    type: Number
  }
})
const $q = useQuasar()
const file = ref()

const emit = defineEmits(['file-uploaded'])

function fileFilter(files) {
  return files.filter(file => {
    if (file.type !== 'application/pdf') {
      $q.notify({
        message: "Файл должен быть в формате PDF",
        color: "negative",
      });
      return false;
    }
    if (file.size > props.maxFileSize) {
      $q.notify({
        message: `Размер файла превышает допустимый лимит (${props.maxFileSize / 1024 / 1024} Мегабайт)`,
        color: "negative",
      });
      return false;
    }
    return true;
  });
}


watch(file, async () => {
  const loadingHelpers = $q.loading.show({
    group: 'third',
    message: 'Загружаю документ',
  })
  const formData = new FormData()
  formData.append('file', file.value)
  formData.append('type', 'document')
  formData.append('fileId', props.fileId)

  let r = await api.post(props.url ? props.url : `/api/upload/${props.planId}/save-file/`, formData)

  emit('file-uploaded')

  let admKey = _.findKey(admissionData.value, (x) => x.plan_id == props.planId)
  admissionData.value[admKey].documents_files.push(r.data)

  loadingHelpers()
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
      style="width: 100%;"
  >
  </q-file>
</template>

<style scoped>

</style>
