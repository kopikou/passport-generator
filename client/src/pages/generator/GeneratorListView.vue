<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import {LocalStorage, SessionStorage, useQuasar} from "quasar";
import {GeneratorListData, GeneratorGroupsList} from "src/types";
import {storeToRefs} from "pinia";
import _ from "lodash";
import useMainStore from "stores/mainStore";
import LayoutHCF from "components/LayoutHCF.vue";
import GeneratorListViewItem from "pages/generator/components/GeneratorListViewItem.vue";
import writeXlsxFile from "write-excel-file";
import dayjs from "dayjs";

const mainStore = useMainStore();
const {
  rop
} = storeToRefs(mainStore)

const $q = useQuasar()
// const listData = ref<GeneratorListData[]>([])

const groupsList = ref<GeneratorGroupsList[]>([]);

const currentProgram = ref([]);
const currentPlan = ref<number>(0);

const tableLoading = ref(false);

const filesButtons = ref({
  rpd: {
    url: 'api/generator/get-rpd-done-info/',
    isLoading: false
  },
  oop: {
    url: 'api/generator/get-oop-done-info/',
    isLoading: false
  }
});

const typeFilterLabel = {
  rop:
    {
      title: 'Руководитель ОП',
      icon: 'mdi mdi-duck',
    },
  fac: {
    title: 'Директор',
    icon: 'mdi mdi-kangaroo',
  },
  zav: {
    title: 'Заведующий кафедры',
    icon: 'mdi mdi-bird',
  },
  person: {
    title: 'Разработчик РПД',
    icon: 'mdi mdi-koala',
  },
  view: {
    title: 'Просмотр РПД',
    icon: 'mdi mdi-linux',
  },
}

const STATUSES = {
  "Назначен": {
    color: "grey-2",
    textColor: "black",
    index: 1,
    title: "Назначен",
  },
  "Заполняется": {
    color: "cyan-5",
    textColor: "white",
    index: 2,
    title: "Заполняется",
  },
  "Требует моего согласования/утверждения": {
    color: "amber-6",
    textColor: "black",
    index: 3,
    title: "Требует моего согласования/утверждения",
  },
  "Отправлен на проверку": {
    color: "light-green-6",
    textColor: "white",
    index: 4,
    title: "Отправлен на проверку",
  },
  "Требуются правки": {
    color: "red-5",
    textColor: "white",
    index: 5,
    title: "Требуются правки",
  },
  "Утвержден": {
    color: "green-5",
    textColor: "white",
    index: 6,
    title: "Утвержден",
  },
}

const statusFilter = ref<string>('');
const groupFilter = ref($q.localStorage.getItem("surp_groupfilter") ? $q.localStorage.getItem("surp_groupfilter") : '')
const discplFilter = ref($q.localStorage.getItem("surp_discplfilter") ? $q.localStorage.getItem("surp_discplfilter") : '')
const myFilter = ref(LocalStorage.getItem('surp_myfilter') || 0)
const textFilter = ref<String>(LocalStorage.getItem('surp_rpdfilter') || '')
const groupTextFilter = ref<String>(LocalStorage.getItem('surp_rpdgroupfilter') || '')
const yearFilter = ref<number>(LocalStorage.getItem('surp_yearfilter') || dayjs().year())

const yearsList = computed(() => {
  let year = 2025;
  let list = []
  while (year <= dayjs().year() + 1) {
    list.push(year);
    year += 1;
  }

  return list;
});

const filteredProgramData = computed(() => {
  let txtFilter = textFilter.value.trim().toLowerCase();
  let data = _(currentProgram.value)
    .filter(x => {
      return (myFilter.value == 0 || x.type.includes('person'))
        && ((txtFilter == '' || x.discode.toLowerCase().includes(txtFilter))
          || (txtFilter == '' || x.discpl.toLowerCase().includes(txtFilter))
          || (txtFilter == '' || x.razrab_name.toLowerCase().includes(txtFilter)))
        && (!statusFilter.value || x.status_verbose == statusFilter.value)
    })
    .value();

    data.forEach(x => x.status = STATUSES[x.status_verbose].index)

    return data
});

async function getGroupsList() {
  const loadProgram = $q.loading.show({
    group: 'programs',
    message: 'Обновление списка дисциплин',
  });

  let r = await api.get("/api/generator/get-group-list/", {
    params: {
      text: textFilter.value,
      groupText: groupTextFilter.value,
      status: statusFilter.value,
      my: myFilter.value,
      year: yearFilter.value,
    },
  });
  groupsList.value = r.data;

  loadProgram();
}

async function getGroupProgram(planId: number) {
  currentPlan.value = planId;

  tableLoading.value = true;

  const r = await api.get(`/api/generator/${planId}/get-group-program/`);
  currentProgram.value = r.data;

  tableLoading.value = false;
}

const updateDataFunction = _.debounce(async () => {
  $q.localStorage.setItem("surp_discplfilter", discplFilter.value)
  $q.localStorage.setItem("surp_groupfilter", groupFilter.value)
  $q.localStorage.setItem("surp_myfilter", myFilter.value)
  $q.localStorage.setItem("surp_rpdfilter", textFilter.value)
  $q.localStorage.setItem("surp_rpdgroupfilter", groupTextFilter.value)

  await getGroupsList();

  if (!currentPlan.value)
    await getGroupProgram(groupsList.value[0].plan_id);
}, 300)

watch([discplFilter, groupFilter, myFilter, textFilter, statusFilter, groupTextFilter, yearFilter], updateDataFunction)

onBeforeMount(async () => {
  await getGroupsList()
  textFilter.value = ''
})

async function getDoneFile(key: string) {
  const fileUrl = filesButtons.value[key]['url'];

  filesButtons.value[key]['isLoading'] = true;

  const response = await api.get(fileUrl);

  let dataRows = [];

  if (key == 'oop') {

    dataRows.push([
      {value: 'Группа', fontWeight: 'bold'},
      {value: 'Уровень', fontWeight: 'bold'},
      {value: 'Доков надо', fontWeight: 'bold'},
      {value: 'Доков сделано', fontWeight: 'bold'},
      {value: 'Учебный план', fontWeight: 'bold'},
      {value: 'Календарный учебный график', fontWeight: 'bold'},
      {value: 'Адаптированный учебный план', fontWeight: 'bold'},
      {value: 'ООП', fontWeight: 'bold'},
      {value: 'АОП', fontWeight: 'bold'},
      {value: 'Программа ГИА', fontWeight: 'bold'},
      {value: 'ФОС ГИА', fontWeight: 'bold'},
      {value: 'Рабочая программа воспитания', fontWeight: 'bold'},
      {value: 'Все документы', fontWeight: 'bold'},
      {value: 'Итог', fontWeight: 'bold'},
    ]);

    response.data.forEach(item => {
      dataRows.push([
        {type: String, value: item.group},
        {type: String, value: item.level},
        {type: Number, value: item.needed_docs},
        {type: Number, value: item.done_docs},
        {type: String, value: item.uch_plan},
        {type: String, value: item.calend_uch_graph},
        {type: String, value: item.adap_uch_plan},
        {type: String, value: item.oop},
        {type: String, value: item.aop},
        {type: String, value: item.pr_gia},
        {type: String, value: item.fos_gia},
        {type: String, value: item.rpv},
        {type: String, value: item.all_docs},
        {type: String, value: item.result},
      ])
    })
  } else if (key == 'rpd') {

    dataRows.push([
      {value: 'Абревиатура', fontWeight: 'bold'},
      {value: 'Всего РПД', fontWeight: 'bold'},
      {value: 'Назначены', fontWeight: 'bold'},
      {value: 'Заполняются', fontWeight: 'bold'},
      {value: 'Отправлены на проверку', fontWeight: 'bold'},
      {value: 'Утверждены', fontWeight: 'bold'},
      {value: 'Требуют правки', fontWeight: 'bold'},
      {value: 'Итог', fontWeight: 'bold'},
    ]);

    response.data.forEach(item => {
      dataRows.push([
        {type: String, value: item.abbr},
        {type: Number, value: item.all_rpds},
        {type: Number, value: item.appointed},
        {type: Number, value: item.is_filled},
        {type: Number, value: item.on_review},
        {type: Number, value: item.accepted},
        {type: Number, value: item.on_refile},
        {type: String, value: item.result},
      ])
    })
  }


  await writeXlsxFile(dataRows, {
    fileName: `${key}.xlsx`,
  });

  filesButtons.value[key]['isLoading'] = false;
}

const columns = [
  { name: 'discode', align: 'center', label: 'Код', field: 'discode', sortable: true },
  { name: 'discpl', align: 'center', label: 'Дисциплина', field: 'discpl', sortable: true },
  { name: 'person', align: 'center', label: 'Составитель', field: 'razrab_name', sortable: true },
  { name: 'kaf', align: 'center', label: 'Кафедра', field: 'kafcode', sortable: true },
  { name: 'rukprog', align: 'center', label: 'Согласовал', field: 'rop_name', sortable: true },
  { name: 'zavkaf', align: 'center', label: 'Утвердил', field: 'zavkaf_name', sortable: true },
  { name: 'status_verbose', align: 'center', label: 'Статус', field: 'status_verbose', sortable: true },
  { name: 'control', align: 'center', label: 'Управление', field: 'type', sortable: false },
];

function rowClassFn (row) {
  return `rpd-row status-${STATUSES[row.status_verbose].index}`;
}

</script>

<template>
  <layout-h-c-f>
    <template #header>
      <div class="q-px-sm q-pb-sm">
        <div class="flex justify-between q-my-sm q-px-sm"
             style="display: grid; grid-template-columns: 1fr 1fr 220px auto auto auto auto; gap: 8px; align-items: center;">
          <q-input outlined label="Поиск по направлению, аббревиатуре, специальности, коду и т.д." v-model="groupTextFilter"
                   clearable @clear="groupTextFilter.value = ''"/>
           <q-input outlined label="Поиск по дисциплине, разработчику программы и т.д." v-model="textFilter"
                   clearable @clear="textFilter.value = ''"/>
          <q-select v-model="statusFilter"
                    label="Статус"
                    :options="_.map(STATUSES)"
                    option-label="title"
                    option-value="title"
                    emit-value
                    map-options
                    clearable
          />

          <q-select
            v-model="yearFilter"
            label="Год"
            :options="yearsList"
          />

          <q-toggle outlined label="Только мои" v-model="myFilter" :true-value="1" :false-value="0"/>

          <q-btn
            icon="mdi-file-excel"
            color="green-6"
            size="md"
            label="РПД"
            target="_blank"
            @click="getDoneFile('rpd')"
            :loading="filesButtons.rpd.isLoading"
            v-if="rop"
          />

          <q-btn
            icon="mdi-file-excel"
            color="green-6"
            size="md"
            label="ООП"
            target="_blank"
            @click="getDoneFile('oop')"
            :loading="filesButtons.oop.isLoading"
            v-if="rop"
          />
        </div>

        <div style="display: flex; flex-wrap: wrap; justify-content: start; gap: 8px;">
          <div v-for="status in STATUSES">
            <q-icon
              :color="status.color"
              name="square"
            />
            {{ status.title }}
          </div>
        </div>
      </div>
    </template>
    <template #content>
         <div v-if="_.size(groupsList) > 0"
           style="display: grid; grid-template-columns: 300px 1fr; overflow: hidden;height: 100%"
      >
        <q-list
          style="overflow-y:auto; height: 100%; box-shadow: 0 0 8px silver; z-index: 100"
          separator
        >
          <q-item
            v-for="value in groupsList"
            style="display: grid; gap: 8px;"
            clickable
            :active="currentPlan === value.plan_id"
            @click="getGroupProgram(value.plan_id)"
            active-class="my-active-item"
          >
            <div style="display: grid; grid-template-columns: 1fr auto">
              <div style="display: flex; justify-content: left; font-size: 1.25rem;">
                {{ `${value.abbr}-${value.yr.toString().slice(-2)}` }}
              </div>

              <div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: right; align-items: center">
                <q-badge v-for="type in value.types" class="animal-icon">
                  <i :class="typeFilterLabel[type].icon" ></i>

                  <q-tooltip style="font-size: 12px; background-color: white; color: black">
                    {{ typeFilterLabel[type].title}}
                  </q-tooltip>
                </q-badge>
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr auto">
              <div class="row">
                <div v-for="(status_value, status) in value.statuses">
                  <q-badge
                    :text-color="STATUSES[status].textColor"
                    :color="STATUSES[status].color"
                    v-if="status_value > 0"
                    style="margin-right: 4px;"
                  >
                    {{ status_value }}
                    <q-tooltip
                      style="font-size: 12px; background-color: white; color: black"
                    >
                      {{ status }}: {{ status_value }}
                    </q-tooltip>
                  </q-badge>
                </div>
              </div>

              <a :href="value.plx_file">*.plx</a>
            </div>

          </q-item>
        </q-list>

           <q-table
              v-if="currentPlan !== 0"
              :rows="filteredProgramData"
              :columns="columns"
              virtual-scroll
              style="overflow-y: auto; height: 100%;"
              wrap-cells
              row-key="discode"
              flat
              bordered
              separator="cell"
              :rows-per-page-options="[0]"
              :table-row-class-fn="rowClassFn"
              table-header-class="table-header"
              :loading="tableLoading"
              loading-label="Загрузка"
          >
            <template  v-slot:body="props">
              <q-tr :props="props">
                <generator-list-view-item @data-updated="getGroupProgram(props.row.plan_id)" :item="props.row"/>
              </q-tr>
            </template>

             <template v-slot:loading>
                <q-inner-loading showing color="primary" />
              </template>
          </q-table>

        <span
          v-else
          style="align-content: center; text-align: center; font-size: 20px; font-weight: bold"
        >
          Выберите нужный раздел слева
        </span>
      </div>

    </template>
  </layout-h-c-f>

</template>

<style scoped lang="scss">
:deep(.table-header) {
  position: sticky;
  z-index: 1;
  top: 0;
  background: $blue-grey-2;
}

.rpd-container {
  display: grid;
  grid-template-columns: auto repeat(5, 1fr) auto auto;
}

:deep(.rpd-row) {
  //display: contents;

  &.status-1 > td { // "Назначен"
    background: white;
  }

  &.status-2 > td { // "Заполняется"
    background: $light-blue-1;
  }

  &.status-3 > td { // "Требует моего согласования/утверждения"
    background: $amber-1;
  }

    &.status-4 > td { // "Отправлен на проверку"
    background: $green-1;
  }

  &.status-5 > td { // "Требуются правки"
    background: $red-1;
  }

  &.status-6 > td { // "Утвержден"
    background: $green-2;
  }




  $border: solid 1px silver;

  > div {
    padding: 0.5rem;
    border: $border;
    border-right: none;
    border-bottom: none;

    &:last-child {
      border-right: $border;
    }
  }

  &:last-child {
    > div {
      border-bottom: $border;
    }
  }

  &.rpd-row__body {
    //&:hover {
    //  > div {
    //    background: $info !important;
    //  }
    //}
  }

}

 :deep(.my-active-item) {
   background: $blue-grey-2;
 }

 :deep(.animal-icon){
   background: $grey-3;
   color: black;
   font-size: 18px;
   padding: 4px;
 }
</style>
