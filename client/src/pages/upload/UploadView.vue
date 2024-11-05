<script setup lang="ts">

import useUploadFileViewStore from "stores/uploadFileViewStore";
import {storeToRefs} from "pinia";
import FileUploader from "pages/upload/components/FileUploader.vue";
import _ from "lodash";

const uploadFileViewStore = useUploadFileViewStore();

const {
  admissionData,
} = storeToRefs(uploadFileViewStore)

async function getFile(planId, fileId) {
  let files = _.filter(admissionData.value, (x) => x.plan_id == planId)[0]?.documents_files
  let url = _.filter(files, (x) => x.type_id == getFileType(planId, fileId))[0]?.file
  if (url) {
    window.location.href = 'uploads/' + url
  }
}

function getFileType(planId, fileId) {
  return _.filter(_.filter(admissionData.value, (x) => x.plan_id == planId)[0].plan_documents, (x) => x.id == fileId)[0].new_type
}

function getColor(planId, fileId) {
  let filesIds = _.map(_.filter(admissionData.value, (x) => x.plan_id == planId)[0]?.documents_files, (x) => x.type_id)
  let type = getFileType(planId, fileId)
  if (filesIds.includes(type)) return 'secondary'
  else return 'negative'
}


</script>

<template>
  <div class="q-pa-lg">
    <div class="text-center text-h6 q-mb-md">Список рабочих программ ИРНИТУ</div>
    <q-list bordered>
      <q-expansion-item
          v-for="item in admissionData"
          expand-separator
          :caption="item.plan_name"
          :label="`Учебный план ${item.abbrprofile} ${item.startyear}`"
      >
        <q-card>
          <q-card-section class="card-body">
            <div class="card-header text-center">
              <div>
                Наименование
              </div>
              <div>
                Загруженные файлы
              </div>
            </div>
            <div class="card-container" v-for="i in item.plan_documents">
              <div>
                {{ i.name }}
              </div>
              <div class="flex items-center" style="display: grid; grid-template-columns: 1fr auto">
                <file-uploader :title="i.new_type__name" :file-id="i.id"/>
                <q-btn
                    icon="mdi-eye"
                    flat
                    dense
                    style="height: 100%"
                    :color="getColor(item.plan_id, i.id)"
                    @click="getFile(item.plan_id, i.id)"
                />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </q-expansion-item>
    </q-list>
  </div>
</template>

<style scoped>

.card-body {

  .card-header {
    display: grid;
    grid-template-columns: 4fr 1fr;
  }

  .card-container {
    display: grid;
    grid-template-columns: 4fr 1fr;
    padding: 5px;
  }
}

</style>
