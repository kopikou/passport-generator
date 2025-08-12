<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {Admission, MonitoringIndicators, RopMonitoring} from "src/types";
import 'src/css/styles.css'
import useRopMonitoringStore from "stores/ropMonitoringStore";
import {storeToRefs} from "pinia";
import LayoutMC from "layouts/LayoutMC.vue";
import RopMonitoringDialog from "components/rop_monitoring/RopMonitoringDialog.vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import _ from "lodash";

const $q = useQuasar()
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

function groupAdmissionList() {
  admissionList.value = _(admissionList.value)
    .groupBy('admission')
    .map((items, admission) => {
      const first = items[0]
      const indicators = items.map(({indicator, value, score}) => ({indicator, value, score}))
      let admissionData = {
        id: first.id,
        rop_monitoring: first.rop_monitoring,
        admission: Number(admission),
        admission_name: first.admission_name,
        person: first.person,
        person_name: first.person_name,
      }

      const indicatorNames = Object.entries(MonitoringIndicators).reduce((acc, [key, val]) => {
        acc[val] = key.toLowerCase();
        return acc;
      }, {});

      indicators.forEach(({indicator, value, score}) => {
        const name = indicatorNames[indicator];
        if (name) {
          admissionData[`${name}_score`] = score;
          admissionData[`${name}_value`] = value;
        }
      });

      return admissionData
    })
    .sortBy('admission_name')
    .value()
}

const filteredMonitoringList = computed(() => {
  const filter = monitoringTextFilter.value?.toLowerCase() || '';
  return ropMonitoringList.value.filter(item =>
    item.name.toLowerCase().includes(filter)
  );
});

const filteredAdmissionList = computed(() => {
  const filter = admissionTextFilter.value?.toLowerCase() || '';
  return admissionList.value.filter(item =>
    (item.admission_name && item.admission_name.toLowerCase().includes(filter)) ||
    (item.person_name && item.person_name.toLowerCase().includes(filter))
  );
});

const selectedRopMonitoringId = ref(0);

const columns = [
  {name: 'name', align: 'center', label: 'Название программы', field: 'admission_name', sortable: true},
  {name: 'rop', align: 'center', label: 'РОП', field: 'person_name', sortable: true},
  {name: 'ege_value', align: 'center', label: 'Ср. балл ЕГЭ (ДВИ)', field: 'ege_value', sortable: true},
  {
    name: 'ege_score',
    align: 'center',
    label: 'Баллы за ср. балл ЕГЭ',
    field: 'ege_score',
    sortable: true
  },
  {
    name: 'stud_contingent_value',
    align: 'center',
    label: 'Доля завершивших/активных студентов',
    field: 'stud_contingent_value',
    sortable: true
  },
  {
    name: 'stud_contingent_score',
    align: 'center',
    label: 'Баллы за долю завершивших/активных студентов',
    field: 'stud_contingent_score',
    sortable: true
  },
  {
    name: 'celev_stud_contingent_value',
    align: 'center',
    label: 'Доля завершивших/активных студентов целевиков',
    field: 'celev_stud_contingent_value',
    sortable: true
  },
  {
    name: 'celev_stud_contingent_score',
    align: 'center',
    label: 'Баллы за долю завершивших/активных студентов целевиков',
    field: 'celev_stud_contingent_score',
    sortable: true
  },
    {
    name: 'npr_value',
    align: 'center',
    label: 'Доля НПР, принявших участие в опросах о кач-ве образ.',
    field: 'npr_value',
    sortable: true
  },
  {
    name: 'npr_score',
    align: 'center',
    label: 'Баллы за долю НПР, принявших участие в опросах о кач-ве образ.',
    field: 'npr_score',
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
  admissionTextFilter.value = '';
  await getAdmissionList();
})

onBeforeMount(async () => {
  if (ropMonitoringList.value.length == 0) {
    await ropMonitoringStore.getRopMonitoringList();
  }
})

function getEgeScoreStyle(value) {
  if (value === 0) {
    return 'bg-pink-11 text-white'
  } else if (value === 1) {
    return 'bg-amber-12 text-white'
  } else if (value === 2) {
    return 'bg-light-green-14 text-white'
  }
  return ''
}

function getContingentScoreStyle(value) {
  if (value === 0) {
    return 'bg-pink-11 text-white'
  } else if (value === 2) {
    return 'bg-amber-12 text-white'
  } else if (value === 4) {
    return 'bg-light-green-14 text-white'
  }
  return ''
}

function getCelevScoreStyle(value) {
  if (value === 0) {
    return 'bg-pink-11 text-white'
  } else if (value === 1) {
    return 'bg-amber-12 text-white'
  } else if (value === 2) {
    return 'bg-light-green-14 text-white'
  }
  return ''
}

function getNprScoreStyle(value) {
  if (value === 0) {
    return 'bg-pink-11 text-white'
  } else if (value === 1) {
    return 'bg-light-green-14 text-white'
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

  let r = await api.get(`api/rop-monitoring-score/`, {
    params: {
      rop_monitoring: selectedRopMonitoringId.value,
    },
  });
  admissionList.value = r.data
  groupAdmissionList();

  loadingAdmissionList.value = false;
}

async function updateAdmissionList() {
  loadingAdmissionList.value = true;
  admissionList.value = [];
  let r = await api.get(`api/rop-monitoring-score/${selectedRopMonitoringId.value}/update-monitoring-data/`);

  if (r.status == 201) {
    admissionList.value = r.data
    groupAdmissionList()
    $q.notify({
      type: 'secondary',
      message: 'Данные обновлены!',
    })
  }

  loadingAdmissionList.value = false;
}

</script>

<template>
  <layout-m-c>
    <template #left-menu>
      <div style="display: grid; grid-template-rows: auto 1fr; overflow: hidden; height: 100%">
        <div style="display: grid; grid-template-columns: 1fr auto; gap: 8px; margin-bottom: 8px">
          <q-input outlined bg-color="white" v-model="monitoringTextFilter" label="Поиск мониторинга"/>
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
        <div style="max-height: 100%; overflow-y: auto">
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
            <template v-slot:body-cell-ege_score="props">
              <q-td :props="props" :class="getEgeScoreStyle(props.value)">
                {{ props.value }}
              </q-td>
            </template>
            <template v-slot:body-cell-stud_contingent_score="props">
              <q-td :props="props" :class="getContingentScoreStyle(props.value)">
                {{ props.value }}
              </q-td>
            </template>
            <template v-slot:body-cell-celev_stud_contingent_score="props">
              <q-td :props="props" :class="getCelevScoreStyle(props.value)">
                {{ props.value }}
              </q-td>
            </template>
            <template v-slot:body-cell-npr_score="props">
              <q-td :props="props" :class="getNprScoreStyle(props.value)">
                {{ props.value }}
              </q-td>
            </template>
          </q-table>
        </div>
      </div>
    </template>
  </layout-m-c>
</template>

<style lang="scss" scoped>
:deep(.q-table thead th) {
  position: sticky;
  top: 0;
  background: white;
  z-index: 10;
}
</style>
