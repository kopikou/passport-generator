<script setup lang="ts">

import useUploadFileViewStore from "stores/uploadFileViewStore";
import {storeToRefs} from "pinia";
import FileUploader from "pages/upload/components/FileUploader.vue";

const uploadFileViewStore = useUploadFileViewStore();

const {
  admissionData,
} = storeToRefs(uploadFileViewStore)

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
              <div class="flex items-center">
                <file-uploader :title="i.new_type__name" :file-id="i.id"/>
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
