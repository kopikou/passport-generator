<script setup lang="ts">
import LayoutHCF from "components/LayoutHCF.vue";
import {onBeforeMount, ref, watch} from "vue";
import {Admission} from "src/types";
import api from "axios";
import 'src/css/styles.css'

let ropMonitorData: any = {};

try {
  ropMonitorData = JSON.parse(localStorage.rop_monitor || '{}')
} catch {
}

const textFilter = ref(ropMonitorData.admissionTextFilter || '');
const loadingAdmissions = ref(false);
const loadingRopMonitoringOptions = ref(false);
const admissions = ref<Admission[]>([]);

const ropMonitoring = ref();
const ropMonitoringOptions = ref([]);

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
  if (ropMonitoringOptions.value.length == 0) {
    await getRopMonitoringOptions();
  }
})

async function getAdmissions() {
  loadingAdmissions.value = true;
  admissions.value = [];
  let r = await api.get('api/rop-monitoring/get-rop-score/');
  admissions.value = r.data;
  loadingAdmissions.value = false;
}

async function getRopMonitoringOptions() {
  loadingRopMonitoringOptions.value = true;
  ropMonitoringOptions.value = [];
  let r = await api.get('api/rop-monitoring/get-rop-score-years/');
  ropMonitoringOptions.value = r.data;
  loadingRopMonitoringOptions.value = false;
}

function getContingentScoreStyle(value) {
  if (value === 0) {
    return 'bg-pink-4 text-white'
  } else if (value === 2) {
    return 'bg-amber-8 text-white'
  } else if (value === 4) {
    return 'bg-green-6 text-white'
  }
  return ''
}

function getCelevScoreStyle(value) {
  if (value === 0) {
    return 'bg-pink-4 text-white'
  } else if (value === 1) {
    return 'bg-amber-8 text-white'
  } else if (value === 2) {
    return 'bg-green-6 text-white'
  }
  return ''
}
</script>

<template>
  <layout-h-c-f>
    <template #header>
      <div class="q-px-sm q-pb-sm">
        <div class="flex justify-between q-my-sm q-px-sm"
             style="display: grid; grid-template-columns: 1fr auto auto; gap: 8px; align-items: center;">
          <q-input outlined label="Поиск по программе или РОПу"
                   v-model="textFilter" :disable="admissions.length == 0" clearable/>
          <q-select v-model="ropMonitoring" outlined
                    label="Мониторинг"
                    :options="ropMonitoringOptions"
                    emit-value
                    map-options
                    clearable
                    :loading="loadingAdmissionYears"
                    :disable="ropMonitoringOptions.length == 0"
                    style="min-width: 200px"
          />
          <div style="display: flex; flex-direction: column; gap: 8px">
            <q-btn
              icon="mdi-format-list-bulleted"
              color="orange-7"
              label="Управление мониторингами"
              @click="getAdmissions"
              :class="{ 'pulse-effect': ropMonitoringOptions.length == 0 }"
            />
            <q-btn
              icon="mdi-creation-outline"
              color="green-7"
              label="Сформировать"
              @click="getAdmissions"
              :disable="!ropMonitoring"
            />
          </div>
        </div>
      </div>
    </template>
    <template #content>
      <div class="q-pa-md" style="height: 100%; overflow-y: hidden">
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
          :hide-bottom="admissions.length > 0"
          style="height: 100%; overflow-y: hidden"
        >
          <template v-slot:body-cell-contingent_students_ratio_score="props">
            <q-td :props="props" :class="getContingentScoreStyle(props.value)">
              {{ props.value }}
            </q-td>
          </template>
          <template v-slot:body-cell-celev_students_ratio_score="props">
            <q-td :props="props" :class="getCelevScoreStyle(props.value)">
              {{ props.value }}
            </q-td>
          </template>
        </q-table>
      </div>
    </template>
  </layout-h-c-f>
</template>

<style scoped>

</style>
