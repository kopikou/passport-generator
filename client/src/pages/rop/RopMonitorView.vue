<script setup lang="ts">
import LayoutHCF from "components/LayoutHCF.vue";
import {onBeforeMount, ref, watch} from "vue";
import {LocalStorage} from "quasar";
import {Admission} from "src/types";
import api from "axios";

let ropMonitorData: any = {};

try {
  ropMonitorData = JSON.parse(localStorage.rop_monitor || '{}')
} catch {
}

const textFilter = ref(ropMonitorData.admissionTextFilter || '');
const loadingAdmissions = ref(false);
const admissions = ref<Admission[]>([]);

const columns = [
  {name: 'name', align: 'center', label: 'Название программы', field: 'name', sortable: true},
  {name: 'rop', align: 'center', label: 'РОП', field: 'rop', sortable: true},
  {name: 'ege_avg_marks', align: 'center', label: 'Ср. балл ЕГЭ (ДВИ)', field: 'ege_avg_marks', sortable: true},
  {
    name: 'ege_avg_marks_score',
    align: 'center',
    label: 'Баллы за ср. балл ЕГЭ',
    field: 'ege_avg_marks_score',
    sortable: true
  },
  {
    name: 'contingent_students_ratio',
    align: 'center',
    label: 'Доля завершивших/активных студентов',
    field: 'contingent_students_ratio',
    sortable: true
  },
  {
    name: 'contingent_students_ratio_score',
    align: 'center',
    label: 'Баллы за долю завершивших/активных студентов',
    field: 'contingent_students_ratio_score',
    sortable: true
  },
  {
    name: 'celev_students_ratio',
    align: 'center',
    label: 'Доля завершивших/активных студентов целевиков',
    field: 'celev_students_ratio',
    sortable: true
  },
  {
    name: 'celev_students_ratio_score',
    align: 'center',
    label: 'Баллы за долю завершивших/активных студентов целевиков',
    field: 'celev_students_ratio_score',
    sortable: true
  },
]

const pagination = ref({
  rowsPerPage: 0,
});

watch(textFilter, () => {
  localStorage.rop_monitor = JSON.stringify({
    admissionTextFilter: textFilter.value,
  })
}, {immediate: true});

onBeforeMount(async () => {
  if(admissions.value.length == 0)
    await getAdmissions();
})

async function getAdmissions() {
  loadingAdmissions.value = true;
  admissions.value = [];
  let r = await api.get('api/rop-monitoring/get-rop-indicators/');
  admissions.value = r.data;
  loadingAdmissions.value = false;
}
</script>

<template>
  <layout-h-c-f>
    <template #header>
      <div class="q-px-sm q-pb-sm">
        <div class="flex justify-between q-my-sm q-px-sm"
             style="display: grid; grid-template-columns: 1fr auto; gap: 8px; align-items: center;">
          <q-input outlined label="Поиск по программе или РОПу"
                   v-model="textFilter" clearable/>
          <q-btn
            icon="mdi-update"
            color="orange-7"
            label="Обновить"
            @click="getAdmissions"
          />
        </div>
      </div>
    </template>
    <template #content>
      <div class="q-pa-md">
        <q-table
          flat bordered
          :rows="admissions"
          :columns="columns"
          row-key="id"
          virtual-scroll
          v-model:pagination="pagination"
          :rows-per-page-options="[0]"
          separator="cell"
          :loading="loadingAdmissions"
          wrap-cells
        />
      </div>
    </template>
  </layout-h-c-f>
</template>

<style scoped>

</style>
