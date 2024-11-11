<script setup lang="ts">

import useUploadFileViewStore from "stores/uploadFileViewStore";
import {storeToRefs} from "pinia";
import FileUploader from "pages/upload/components/FileUploader.vue";
import _ from "lodash";
import {api} from "boot/axios";
import {useQuasar} from "quasar";

const $q = useQuasar()
const uploadFileViewStore = useUploadFileViewStore();

const {
  admissionData,
} = storeToRefs(uploadFileViewStore)

function getFileUrl(planId, fileId) {
  let files = _.filter(admissionData.value, (x) => x.plan_id == planId)[0]?.documents_files
  let url = _.filter(files, (x) => x.type_id == getFileType(planId, fileId))[0]?.file
  if (url) {
    window.location.href = 'uploads/' + url
  }
}

function getFileId(planId, fileId) {
  let files = _.filter(admissionData.value, (x) => x.plan_id == planId)[0]?.documents_files
  return _.filter(files, (x) => x.type_id == getFileType(planId, fileId))[0]?.id
}

function getFileType(planId, fileId) {
  return _.filter(_.filter(admissionData.value, (x) => x.plan_id == planId)[0].plan_documents, (x) => x.id == fileId)[0].new_type
}

async function deleteFile(planId, id) {
  $q.dialog({
    title: 'Удаление файла',
    message: 'Вы точно хотите удалить выбранный файл?',
    ok: {
      label: 'Удалить',
      flat: true,
      color: 'red',
    },
    cancel: {
      label: 'Отмена',
      flat: true,
      color: 'green',
    },
    persistent: true
  }).onOk(async () => {
    $q.loading.show()
    let r = await api.delete(`/api/upload/${id}/`)
    let admKey = _.findKey(admissionData.value, (x) => x.plan_id == planId)
    let fileKey = _.findKey(admissionData.value[admKey].documents_files, (x) => x.id == id)
    admissionData.value[admKey].documents_files.splice(fileKey, 1)
    $q.loading.hide()
  })
}

function checkFile(planId, fileId) {
  let filesIds = _.map(_.filter(admissionData.value, (x) => x.plan_id == planId)[0]?.documents_files, (x) => x.type_id)
  let type = getFileType(planId, fileId)
  if (filesIds.includes(type)) return true
  else return false
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
                <div v-if="!checkFile(item.plan_id, i.id)">
                  <file-uploader :title="i.new_type__name" :file-id="i.id" :plan-id="item.plan_id"/>
                </div>
                <div v-else>
                  <q-field
                      outlined
                      stack-label
                      dense
                      bg-color="green-3"
                  >
                    <template v-slot:control>
                      {{ i.name }}
                    </template>
                    <template v-slot:append>
                      <q-btn
                          icon="mdi-eye"
                          flat
                          dense
                          style="height: 100%"
                          v-show="checkFile(item.plan_id, i.id)"
                          color="secondary"
                          @click="getFileUrl(item.plan_id, i.id)"
                      />
                    </template>
                  </q-field>
                </div>
                <q-btn v-show="checkFile(item.plan_id, i.id)" flat dense icon="mdi-delete" color="negative"
                       @click="deleteFile(item.plan_id, getFileId(item.plan_id, i.id))"/>
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
