<script setup lang="ts">

import useUploadFileViewStore from "stores/uploadFileViewStore";
import {storeToRefs} from "pinia";

const uploadFileViewStore = useUploadFileViewStore();

const {
  admissionData,
} = storeToRefs(uploadFileViewStore)

</script>

<template>
  <div class="q-pa-lg">
    {{admissionData}}
    <div class="text-center text-h6 q-mb-md">Список рабочих программ ИРНИТУ</div>
    <q-list bordered>
      <q-expansion-item
          v-for="item in admissionData"
          expand-separator
          :caption="item.plan_name"
          :label="`Учебный план ${item.abbrprofile} ${item.startyear}`"
      >
        <q-card>
          <q-card-section>
            {{ item.plan_documents }}
          </q-card-section>
        </q-card>
      </q-expansion-item>
    </q-list>
  </div>
</template>

<style scoped>

</style>
