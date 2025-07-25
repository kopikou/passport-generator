<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {Admission, RopMonitoring} from "src/types";
import 'src/css/styles.css'
import useRopMonitoringStore from "stores/ropMonitoringStore";
import {storeToRefs} from "pinia";
import LayoutMC from "layouts/LayoutMC.vue";
import RopMonitoringDialog from "components/rop_monitoring/RopMonitoringDialog.vue";
import {api} from "boot/axios";

const popup = ref(null);
const ropMonitoringStore = useRopMonitoringStore();
const {
  ropMonitoringList,
  loadingRopMonitoringList,
} = storeToRefs(ropMonitoringStore);

let ropMonitoringFilters: any = {};

try {
  ropMonitoringFilters = JSON.parse(localStorage.rop_monitoring_filters || '{}');
} catch {
}

const admissionTextFilter = ref(ropMonitoringFilters.ropTextFilter || '');
const monitoringTextFilter = ref(ropMonitoringFilters.monitoringTextFilter || '');
const loadingAdmissionList = ref(false);
const admissionList = ref<Admission[]>([]);

const filteredMonitoringList = computed(() => {
  const filter = monitoringTextFilter.value.toLowerCase();
  return ropMonitoringList.value.filter(item =>
    item.name.toLowerCase().includes(filter)
  );
});
const filteredAdmissionList = computed(() => {
  const filter = admissionTextFilter.value.toLowerCase();
  return admissionList.value.filter(item =>
    item.name.toLowerCase().includes(filter)
  );
});

const selectedRopMonitoringId = ref(0);

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

watch([admissionTextFilter, monitoringTextFilter], () => {
  localStorage.rop_monitoring_filters = JSON.stringify({
    ropTextFilter: admissionTextFilter.value,
    monitoringTextFilter: monitoringTextFilter.value,
  })
}, {immediate: true});

watch(selectedRopMonitoringId, async () => {
  await getAdmissionList();
})

onBeforeMount(async () => {
  if (ropMonitoringList.value.length == 0) {
    await ropMonitoringStore.getRopMonitoringList();
  }
})

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

function setSelectedMonitoring(monitoringId: number) {
  if (selectedRopMonitoringId.value != monitoringId)
    selectedRopMonitoringId.value = monitoringId
  else
    selectedRopMonitoringId.value = 0
}

async function getAdmissionList() {
  loadingAdmissionList.value = true;
  admissionList.value = [];

  let r = await api.get('api/')

  loadingAdmissionList.value = false;
}

async function updateAdmissionList() {
  loadingAdmissionList.value = true;
  admissionList.value = [];

  loadingAdmissionList.value = false;
}

</script>

<template>
  <layout-m-c>
    <template #left-menu>
      <div style="display: grid; grid-template-rows: auto 1fr; overflow: hidden; height: 100%">
        <div style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 8px">
          <q-input outlined bg-color="white" v-model="monitoringTextFilter" label="Название"/>
          <q-btn icon="mdi-plus" color="green-5">
            <q-popup-edit
              v-model="popup"
              auto-save
              v-slot="scope"
              :offset="[5, 0]"
              :cover="false"
              anchor="center right"
              self="center left"
              style="box-shadow: 0 8px 20px rgba(0, 0, 0, 0.7); border: solid grey 1px"
            >
              <rop-monitoring-dialog/>
            </q-popup-edit>
          </q-btn>
        </div>
        <div style="overflow-y: auto;">
          <q-list bordered separator>
            <q-item v-for="monitoring in filteredMonitoringList" :key="monitoring.id"
                    clickable
                    :active="selectedRopMonitoringId === monitoring.id"
                    @click="setSelectedMonitoring(monitoring.id)"
                    class="q-pa-sm"
                    active-class="active-item"
            >
              <q-item-section>
                <q-item-label lines="1" style="text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">
                  {{ monitoring.name }}
                </q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </div>
        <q-inner-loading :showing="loadingRopMonitoringList">
          <q-spinner-gears color="primary"/>
        </q-inner-loading>
      </div>
    </template>
    <template #content>
      <div style="height: 100%; overflow: hidden; display: grid; grid-template-rows: auto 1fr">
        <div class="q-my-sm" style="display: grid; grid-template-columns: 1fr auto; gap: 8px; align-items: center;">
          <q-input outlined label="Поиск по программе или РОПу"
                   v-model="admissionTextFilter" :disable="admissionList.length == 0" clearable/>
          <q-btn
            icon="mdi-creation-outline"
            color="green-7"
            label="Обновить данные"
            @click="updateAdmissionList"
            :disable="!selectedRopMonitoringId"
            style="height: 100%"
          />
        </div>
        <div style="overflow-y: auto">
          <q-table
            flat bordered
            :rows="filteredAdmissionList"
            :columns="columns"
            row-key="id"
            virtual-scroll
            v-model:pagination="pagination"
            :rows-per-page-options="[0]"
            separator="cell"
            :loading="loadingAdmissionList"
            wrap-cells
            :hide-bottom="admissionList.length > 0"
            style="height: 100%;"
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
      </div>
    </template>
  </layout-m-c>
</template>

<style scoped>

</style>
